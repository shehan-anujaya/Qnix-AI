# Qnix AI - Python Backend

AI-Powered Knowledge Archive backend using FastAPI, Ollama, and ChromaDB.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+** installed
2. **Ollama** installed and running ([Download Ollama](https://ollama.ai))
3. Required Ollama models pulled:
   ```bash
   ollama pull qwen2.5:3b
   ollama pull nomic-embed-text
   ```

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

```bash
# Development mode with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python app/main.py
```

The server will start at: **http://localhost:8000**

API documentation available at: **http://localhost:8000/docs**

## 📚 API Endpoints

### Health Check
- `GET /api/health` - Check backend and Ollama status
- `GET /api/health/ollama` - Detailed Ollama service check

### Documents
- `POST /api/documents/upload` - Upload and process PDF
- `GET /api/documents/list` - List all uploaded documents
- `DELETE /api/documents/{file_id}` - Delete a document

### Chat
- `POST /api/chat/ask` - Ask a question (RAG-based)
- `POST /api/chat/summarize` - Generate document summary (coming soon)
- `POST /api/chat/generate-mcq` - Generate MCQs (coming soon)

## 🏗️ Architecture

### RAG Pipeline

1. **Document Ingestion** (`app/rag/ingest.py`)
   - Extract text from PDF
   - Chunk text with overlap (1000 chars, 200 overlap)
   - Generate embeddings using `nomic-embed-text`
   - Store in ChromaDB

2. **Query Processing** (`app/rag/query.py`)
   - Generate question embedding
   - Retrieve top-k similar chunks
   - Construct prompt with context
   - Generate answer using `qwen2.5:3b`

3. **Vector Store** (`app/db/vector_store.py`)
   - ChromaDB for persistent vector storage
   - Similarity search for retrieval
   - Document metadata tracking

### Project Structure

```
backend_python/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/                 # API endpoints
│   │   ├── health.py        # Health checks
│   │   ├── documents.py     # Document management
│   │   └── chat.py          # Chat/QA endpoints
│   ├── rag/                 # RAG pipeline
│   │   ├── ingest.py        # PDF ingestion
│   │   ├── query.py         # Query processing
│   │   └── prompts.py       # LLM prompts
│   ├── db/                  # Database layer
│   │   └── vector_store.py  # ChromaDB integration
│   └── utils/               # Utilities
│       ├── pdf_utils.py     # PDF extraction
│       └── ollama_client.py # Ollama API client
├── data/                    # Data storage (created at runtime)
│   ├── uploads/             # Uploaded PDFs
│   └── chroma_db/           # Vector database
└── requirements.txt         # Python dependencies
```

## 🔧 Configuration

### Ollama Models

The backend uses:
- **Chat Model**: `qwen2.5:3b` (lightweight, fast)
- **Embedding Model**: `nomic-embed-text`

To use different models, edit `app/utils/ollama_client.py`:
```python
CHAT_MODEL = "qwen2.5:3b"  # Change to your preferred model
EMBEDDING_MODEL = "nomic-embed-text"
```

### Chunking Strategy

Adjust chunking parameters in `app/rag/ingest.py`:
```python
CHUNK_SIZE = 1000      # Characters per chunk
CHUNK_OVERLAP = 200    # Overlap between chunks
```

## 🧪 Testing

### Test Health Endpoint
```bash
curl http://localhost:8000/api/health
```

### Test Document Upload
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@/path/to/document.pdf"
```

### Test Chat
```bash
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of the document?"}'
```

## 🐛 Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check Ollama is accessible: `curl http://localhost:11434/api/tags`
- Verify models are installed: `ollama list`

### ChromaDB Issues
- Delete `data/chroma_db/` to reset vector store
- Ensure write permissions in project directory

### PDF Processing Errors
- Ensure PDF is text-based (not scanned images)
- Check PDF is not password-protected
- Verify sufficient disk space for uploads

## 📝 Development Notes

- **Offline-first**: No external API calls, all processing local
- **Production-ready**: Proper error handling and logging
- **Scalable**: Easy to add new endpoints and features
- **Well-documented**: Comprehensive docstrings and comments

## 🔮 Future Enhancements

- [ ] Document summarization
- [ ] MCQ generation
- [ ] Sinhala language support
- [ ] User authentication
- [ ] Document versioning
- [ ] Advanced search filters
- [ ] Export chat history

## 📄 License

MIT License - See LICENSE file for details
