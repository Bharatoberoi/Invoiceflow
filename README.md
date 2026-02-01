# InvoiceFlow

**AI-Powered Orders & Invoices Assistant**

InvoiceFlow is a sophisticated chatbot that leverages LangGraph, LLMs, and RAG (Retrieval Augmented Generation) to provide intelligent insights about your orders and invoices.

## Features

- 🤖 **AI-Powered Assistant**: Uses LLaMA 3.2 via Ollama for natural language understanding
- 📄 **PDF Processing**: Automatically processes PDF documents from orders and invoices
- 🔍 **Semantic Search**: Utilizes HuggingFace embeddings for intelligent document retrieval
- 💬 **Interactive Chat**: Beautiful web interface for conversation
- 🏗️ **LangGraph Agent**: Sophisticated agent routing for order and invoice queries
- 🗄️ **Vector Database**: ChromaDB for efficient document storage and retrieval

## Prerequisites

- Python 3.11+
- Docker (for Cloud Run deployment)
- Google Cloud Account (for deployment)
- Ollama with llama3.2 model running locally (for local development)

## Local Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/invoiceflow.git
cd invoiceflow
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure Ollama is running with llama3.2:
```bash
ollama run llama3.2
```

5. Run the server:
```bash
python server.py
```

6. Open your browser to `http://localhost:5000`

## API Endpoints

- `GET /` - Serves the web interface
- `GET /api/health` - Health check endpoint
- `POST /api/chat` - Send a message to the chatbot
- `POST /api/reset` - Reset conversation history
- `GET /api/history` - Get conversation history

## Cloud Run Deployment

### Prerequisites

- Google Cloud SDK installed
- Authenticated with `gcloud auth login`
- A Google Cloud project

### Deploy

1. Create a repository and push code to GitHub:
```bash
git remote add origin https://github.com/yourusername/invoiceflow.git
git branch -M main
git push -u origin main
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy invoiceflow \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --timeout 3600
```

3. Access your deployment at the provided URL

## Project Structure

```
invoiceflow/
├── server.py              # Main Flask application
├── app.py                 # LangGraph agent logic
├── index.html             # Web UI
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── invoices/              # Invoice PDFs
├── orders/                # Order PDFs
├── chroma_db/             # Vector database storage
└── TESTING_GUIDE.md       # Testing documentation
```

## Sample Queries

- "What orders do we have?"
- "Show me invoice details"
- "Check status of order ORD-001"
- "Tell me about the latest orders"
- "What's the shipping information for order ABC-123?"

## Architecture

InvoiceFlow uses a LangGraph-based architecture with:

1. **Query Classification**: Routes queries to appropriate handlers
2. **Order Agent**: Handles order-related queries with search tools
3. **Invoice Agent**: Handles invoice-related queries
4. **General Agent**: Handles general conversation
5. **RAG Pipeline**: Retrieves relevant documents from the vector database

## Technologies

- **LangChain**: LLM orchestration framework
- **LangGraph**: Agent graph framework
- **Ollama**: Local LLM inference
- **ChromaDB**: Vector database
- **HuggingFace**: Embeddings and models
- **Flask**: Web framework
- **Sentence Transformers**: Text embeddings

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

## Support

For questions and support, please open an issue on GitHub.
