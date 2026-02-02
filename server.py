"""Simple Flask server to expose the chatbot as an API"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

from langchain.tools import tool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

PERSIST_DIR = "chroma_db"

# Lazy-loaded resources
invoice_vectordb = None
order_vectordb = None
orders_retriever = None
invoices_retriever = None
resources_ready = False
resources_error = None

def load_and_split_pdfs(folder_path):
    """Load PDFs from folder and split into chunks."""
    if not os.path.exists(folder_path):
        logger.warning(f"Folder {folder_path} does not exist. Creating it...")
        os.makedirs(folder_path, exist_ok=True)
        return []
    
    docs = []
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {folder_path}")
        return []
    
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    for file in pdf_files:
        try:
            file_path = os.path.join(folder_path, file)
            logger.info(f"Loading {file}...")
            loader = PyPDFLoader(file_path)
            file_docs = loader.load()
            docs.extend(file_docs)
            logger.info(f"Loaded {len(file_docs)} pages from {file}")
        except Exception as e:
            logger.error(f"Error loading {file}: {str(e)}")
    
    if not docs:
        logger.warning("No documents were loaded successfully")
        return []
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    
    split_docs = splitter.split_documents(docs) 
    return split_docs

def create_or_load_vectorstore(documents=None, name="docs"):
    model_name = "BAAI/bge-small-en-v1.5"
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    if not documents:
        logger.info("[INFO] No documents provided. Creating empty Chroma collection...")
        return Chroma(
            collection_name=name,
            embedding_function=embeddings,
            persist_directory=PERSIST_DIR,
        )

    logger.info("[INFO] Creating ChromaDB and embedding documents...")
    vectordb = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=PERSIST_DIR,
        collection_name=name,
    )
    vectordb.persist()
    return vectordb

def extract_tool_arg(tool_args, key, fallback=None):
    """Extract a string argument from tool call payloads, handling schema-wrapped values."""
    value = tool_args
    if isinstance(tool_args, dict):
        value = tool_args.get(key, tool_args)

    if isinstance(value, dict):
        if "value" in value:
            return value.get("value", fallback)
        if "content" in value:
            return value.get("content", fallback)

    return value if value is not None else fallback

def init_resources():
    """Load embeddings and vector stores on first use."""
    global invoice_vectordb, order_vectordb, orders_retriever, invoices_retriever
    global resources_ready, resources_error

    if resources_ready:
        return True
    if resources_error:
        return False

    try:
        print("[INFO] Loading documents and initializing vector stores...")
        invoice_docs = load_and_split_pdfs("invoices")
        order_docs = load_and_split_pdfs("orders")
        invoice_vectordb = create_or_load_vectorstore(invoice_docs, "invoices_pdfs")
        order_vectordb = create_or_load_vectorstore(order_docs, "orders_pdfs")
        orders_retriever = order_vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        invoices_retriever = invoice_vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        resources_ready = True
        return True
    except Exception as exc:
        resources_error = str(exc)
        logger.error(f"Failed to initialize resources: {resources_error}", exc_info=True)
        return False

@tool
def search_orders(query: str) -> str:
    """Search the orders PDFs for information on order details, shipping details, customer details, shipper details, products and number of orders """
    if not init_resources():
        return f"Resources not ready: {resources_error or 'initializing'}"
    logger.info(f"Searching orders for: {query}")
    docs = orders_retriever.invoke(query)
    if not docs:
        return "No matches found."
    chunks = []
    for i, d in enumerate(docs, 1):
        meta = d.metadata or {}
        src = meta.get("source", "unknown")
        page = meta.get("page", None)
        where = f" (page {page})" if page is not None else ""
        chunks.append(f"[{i}] {src}{where}:\n{d.page_content[:800]}")
    return "\n\n".join(chunks)

@tool
def search_invoices(query: str) -> str:
    """Search the invoices PDFs for information on invoice details"""
    if not init_resources():
        return f"Resources not ready: {resources_error or 'initializing'}"
    logger.info(f"Searching invoices for: {query}")
    docs = invoices_retriever.invoke(query)
    if not docs:
        return "No matches found."
    chunks = []
    for i, d in enumerate(docs, 1):
        meta = d.metadata or {}
        src = meta.get("source", "unknown")
        page = meta.get("page", None)
        where = f" (page {page})" if page is not None else ""
        chunks.append(f"[{i}] {src}{where}:\n{d.page_content[:800]}")
    return "\n\n".join(chunks)

@tool("get_order_status", return_direct=False, description="Get the order status of an order id")
def get_order_status(order_id: str) -> str:
    statuses = ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]
    idx = sum(ord(c) for c in order_id) % len(statuses)
    return f"Order {order_id} status: {statuses[idx]}"

class QueryType(BaseModel):
    query_type: Literal["invoice","order","general"] = Field(
        ...,
        description="Classify if the message was a query about invoices, orders or a general query."
    )

class State(TypedDict):
    messages: Annotated[list, add_messages]
    query_type: str | None

llm = ChatOllama(model="llama3.2", temperature=0.7)

orders_tools = [search_orders, get_order_status]
invoices_tools = [search_invoices]

def classify_query(state: State):
    message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(QueryType)
    result = classifier_llm.invoke([
        {
            "role" : "system",
            "content" : """Classify the user message as either questions on invoices, orders or general.
            - 'order': If the user asks about an order or the query has the word order or orders in it.
            - 'invoice': If the user asks about an invoice or the query has the word invoice or invoices
            - 'general' : If the user asks anything other than about invoices or orders """
        },
        {
            "role" : "user",
            "content" : message.content
        }
    ])
    return {"query_type": result.query_type}

def router(state: State):
    query_type = state.get("query_type" , "general")
    if query_type == "order":
        return {"next" : "order"}
    elif query_type == "invoice":
        return {"next" : "invoice"}
    return {"next" : "general"}

def orders_agent(state: State):
    llm_with_tools = llm.bind_tools(orders_tools)
    messages = state["messages"]
    
    response = llm_with_tools.invoke(messages)
    messages = messages + [response]
    
    if response.tool_calls:
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            try:
                if tool_name == "search_orders":
                    fallback_query = state["messages"][-1].content if state.get("messages") else ""
                    query = extract_tool_arg(tool_args, "query", fallback=fallback_query)
                    result = search_orders.invoke({"query": str(query)})
                elif tool_name == "get_order_status":
                    fallback_order = state["messages"][-1].content if state.get("messages") else ""
                    order_id = extract_tool_arg(tool_args, "order_id", fallback=fallback_order)
                    result = get_order_status.invoke({"order_id": str(order_id)})
                else:
                    result = f"Unknown tool: {tool_name}"
            except Exception as e:
                logger.error(f"Tool error: {str(e)}", exc_info=True)
                result = f"Error calling tool: {str(e)}"
            
            tool_message = ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
            tool_messages.append(tool_message)
            messages = messages + [tool_message]
        
        final_response = llm.invoke(messages)
        return {"messages": messages + [final_response]}
    else:
        return {"messages": messages}

def general_agent(state: State):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": messages + [response]}

def invoices_agent(state: State):
    llm_with_tools = llm.bind_tools(invoices_tools)
    messages = state["messages"]
    
    response = llm_with_tools.invoke(messages)
    messages = messages + [response]
    
    if response.tool_calls:
        tool_messages = []
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            try:
                if tool_name == "search_invoices":           
                    fallback_query = state["messages"][-1].content if state.get("messages") else ""
                    query = extract_tool_arg(tool_args, "query", fallback=fallback_query)
                    result = search_invoices.invoke({"query": str(query)})
                else:
                    result = f"Unknown tool: {tool_name}"
            except Exception as e:
                logger.error(f"Tool error: {str(e)}", exc_info=True)
                result = f"Error calling tool: {str(e)}"
            
            tool_message = ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
            tool_messages.append(tool_message)
            messages = messages + [tool_message]
        
        final_response = llm.invoke(messages)
        return {"messages": messages + [final_response]}
    else:
        return {"messages": messages}

# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("classifier", classify_query)
graph_builder.add_node("router", router)
graph_builder.add_node("order", orders_agent)
graph_builder.add_node("invoice", invoices_agent)
graph_builder.add_node("general", general_agent)

graph_builder.add_edge(START, "classifier")
graph_builder.add_edge("classifier", "router")
graph_builder.add_conditional_edges("router",
    lambda state: state.get("next"),
    {"order":"order","invoice":"invoice","general":"general"}
)
graph_builder.add_edge("order", END)
graph_builder.add_edge("invoice", END)
graph_builder.add_edge("general", END)

graph = graph_builder.compile()

# Global state for conversation
conversation_state = {"messages": [], "query_type": None}

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    if not resources_ready and not resources_error:
        init_resources()
    return jsonify({
        'status': 'ok' if resources_ready else 'initializing',
        'ready': resources_ready,
        'error': resources_error
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    global conversation_state
    
    if not resources_ready:
        return jsonify({'error': 'Server still initializing, please wait...'}), 503
    
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    try:
        # Add user message to state
        user_msg = HumanMessage(content=user_message)
        conversation_state["messages"] = conversation_state.get("messages", []) + [user_msg]
        
        # Invoke the graph
        result = graph.invoke(conversation_state)
        conversation_state = result
        
        # Extract assistant response
        if result.get("messages") and len(result["messages"]) > 0:
            last_message = result["messages"][-1]
            if hasattr(last_message, 'content'):
                response_text = last_message.content
            else:
                response_text = str(last_message)
        else:
            response_text = "No response generated"
        
        return jsonify({
            'status': 'success',
            'response': response_text,
            'query_type': result.get('query_type')
        })
    
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation"""
    global conversation_state
    conversation_state = {"messages": [], "query_type": None}
    return jsonify({'status': 'success', 'message': 'Conversation reset'})

@app.route('/api/history', methods=['GET'])
def history():
    """Get conversation history"""
    global conversation_state
    
    history = []
    for msg in conversation_state.get("messages", []):
        if isinstance(msg, HumanMessage):
            history.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            history.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, ToolMessage):
            history.append({"role": "tool", "content": msg.content})
    
    return jsonify({'history': history})

@app.route('/')
def index():
    """Serve the frontend UI"""
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
def index_explicit():
    """Serve the frontend UI - explicit route"""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    print("[INFO] Pre-loading resources at startup...")
    init_resources()
    if resources_ready:
        print("[INFO] ✓ Resources loaded successfully!")
    else:
        print(f"[WARNING] Resources failed to load: {resources_error}")
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    print(f"[INFO] Starting Flask server on http://localhost:{port}")
    print(f"[INFO] Open http://localhost:{port} in your browser")
    app.run(debug=False, host='0.0.0.0', port=port)
