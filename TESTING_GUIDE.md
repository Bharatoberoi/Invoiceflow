# InvoiceFlow Frontend & Testing Guide

## Quick Start

### 1. Install Flask and dependencies
```bash
pip install flask flask-cors
```

### 2. Start the backend server
```bash
python server.py
```

You should see:
```
[INFO] Starting Flask server on http://localhost:5000
```

### 3. Open the frontend
Open `index.html` in your browser:
- Simply double-click the file, or
- Use a local server: `python -m http.server 8000` and visit `http://localhost:8000/index.html`

---

## Sample Queries to Try

### **Order Queries** 🛒
These will trigger the `search_orders` tool and RAG retrieval from order PDFs:

1. **"What orders do we have?"**
   - Generic order inquiry that triggers RAG search
   - Returns relevant order documents from the vector database

2. **"Show me order details"**
   - Requests detailed information about orders
   - Searches the order PDFs for comprehensive details

3. **"Tell me about the latest orders"**
   - Specific query about recent orders
   - Retrieves order documents with temporal context

4. **"Check status of order ORD-001"**
   - Specific order status request
   - Triggers `get_order_status` tool for status lookup
   - Returns: PENDING, PROCESSING, SHIPPED, DELIVERED, or CANCELLED

5. **"What's the shipping information for order ABC-123?"**
   - Queries shipping details
   - Uses RAG to search order PDFs for shipping information

### **Invoice Queries** 📄
These will trigger the `search_invoices` tool and RAG retrieval from invoice PDFs:

1. **"What invoice details do we have?"**
   - General invoice inquiry
   - Returns matching invoice documents

2. **"Show me invoice information"**
   - Requests invoice details
   - Retrieves relevant invoice PDFs

3. **"Tell me about recent invoices"**
   - Specific query about recent invoices
   - Searches for temporally relevant invoices

4. **"What are the invoice amounts?"**
   - Queries invoice financial information
   - Uses RAG to extract invoice amounts

5. **"Show me invoice INV-2024-001"**
   - Specific invoice lookup
   - Retrieves detailed invoice information

### **General Queries** 💬
These will use the general agent (no tool calling):

1. **"Hello, how can you help?"**
   - Greeting and capability overview
   - Returns assistant's introduction

2. **"What can you do?"**
   - Asks about chatbot capabilities
   - Explains available features

3. **"How do I check my orders?"**
   - Questions about usage
   - Provides guidance

4. **"Tell me about this system"**
   - System overview request
   - Explains the InvoiceFlow architecture

5. **"What information do you have access to?"**
   - Access permission questions
   - Describes available data sources (orders and invoices)

---

## Architecture Overview

### Backend (server.py)
- **Flask API** serving on `http://localhost:5000`
- **Endpoints:**
  - `POST /api/chat` - Send a message, get response
  - `POST /api/reset` - Clear conversation history
  - `GET /api/history` - Get conversation history

- **Components:**
  - **LangGraph Workflow:** Multi-node graph (classify → route → specialized agents)
  - **Query Classification:** Uses LLM with structured output to categorize queries
  - **RAG Tools:** `search_orders`, `search_invoices` using Chroma vector DB
  - **API Tool:** `get_order_status` for order status lookups
  - **LLM:** Ollama llama3.2 model (local inference)

### Frontend (index.html)
- **Beautiful Chat UI** with gradient design
- **Sidebar:** Quick access to 10+ sample queries
- **Features:**
  - Real-time message display with animations
  - Loading indicators
  - Message history with different styling for user/assistant/tool messages
  - One-click sample queries
  - Clear conversation button
  - Responsive design (works on mobile)

### Vector Database (Chroma)
- **Orders Collection:** Stores order PDF embeddings
- **Invoices Collection:** Stores invoice PDF embeddings
- **Embedding Model:** BAAI/bge-small-en-v1.5 (HuggingFace)
- **Persistence:** `chroma_db/` directory

---

## Troubleshooting

### **Frontend won't connect to backend**
- Make sure server.py is running
- Check that Flask is listening on `localhost:5000`
- Look for CORS issues in browser console (F12)

### **"No matches found" responses**
- PDF folders might be empty
- Check that `invoices/` and `orders/` folders have PDF files
- Verify PDFs are readable (not corrupted)

### **Slow first query**
- First query loads the embedding model (~133MB)
- This is normal and only happens once

### **Tool not being called**
- Check the Query Classification node classified correctly
- Look at server console logs for debug info
- Verify tool arguments are being extracted properly

### **Empty responses**
- Check Ollama is running: `ollama serve`
- Verify llama3.2 model is downloaded: `ollama list`
- Check network connection between app and Ollama

---

## Testing Workflow

1. **Start fresh:**
   - Click "Clear Chat" button in sidebar
   - Server resets conversation state

2. **Test classification:**
   - Try an order query and watch how it's routed
   - Tool results show "[Query Type: order]" confirmation

3. **Test RAG retrieval:**
   - Order query returns matching document chunks from PDFs
   - Notice page numbers and source file references

4. **Test tool calling:**
   - Status check queries trigger the `get_order_status` tool
   - Demonstrates LLM tool selection and execution

5. **Test general chat:**
   - Non-specific queries use general agent
   - No tool calling, just LLM conversation

---

## API Reference

### POST /api/chat
Send a user message and get a response.

**Request:**
```json
{
  "message": "What orders do we have?"
}
```

**Response:**
```json
{
  "status": "success",
  "response": "Based on the search, we have...",
  "query_type": "order"
}
```

### POST /api/reset
Reset the conversation history.

**Response:**
```json
{
  "status": "success",
  "message": "Conversation reset"
}
```

### GET /api/history
Get the full conversation history.

**Response:**
```json
{
  "history": [
    {"role": "user", "content": "What orders do we have?"},
    {"role": "assistant", "content": "..."},
    {"role": "tool", "content": "..."}
  ]
}
```

---

## File Structure

```
Langraph_chatbot/
├── app.py              # Original CLI application
├── server.py           # Flask API server
├── index.html          # Frontend chat UI
├── test_input.txt      # Sample test queries
├── invoices/           # Invoice PDF folder
│   ├── invoice_1.pdf
│   └── invoice_2.pdf
├── orders/             # Order PDF folder
│   ├── order_1.pdf
│   └── order_2.pdf
├── chroma_db/          # Vector database storage
└── .venv/              # Python virtual environment
```

---

## Tips for Best Results

- **Be specific:** "Show me invoice details" works better than just "invoices"
- **Use keywords:** Include "order" or "invoice" for better classification
- **Complete queries:** Full sentences work better than fragments
- **Check logs:** Server console shows detailed execution trace
- **Try variations:** Different wordings trigger different retrieval results

Enjoy testing the chatbot!
