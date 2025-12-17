# Qnix AI - AI-Powered Knowledge Archive

**Desktop Application for Sri Lankan Students**

A production-ready, offline-first desktop application that uses local LLM (via Ollama) to provide intelligent question-answering based on uploaded study materials.

![Flutter](https://img.shields.io/badge/Flutter-Desktop-02569B?logo=flutter)
![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?logo=python)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000)

---

## 🌟 Features

- **📚 Document Management**: Upload and manage PDF study materials
- **💬 AI Chat**: Ask questions and get answers based on your documents
- **🔍 RAG Pipeline**: Retrieval Augmented Generation for accurate responses
- **🌙 Dark Mode**: Beautiful Material 3 dark theme
- **🔒 Offline-First**: No internet required, all processing is local
- **🚀 Fast & Efficient**: Optimized for desktop performance
- **🎓 Student-Friendly**: Designed specifically for Sri Lankan students

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Flutter Desktop UI                     │
│  (Material 3, Chat Interface, Document Manager)         │
└────────────────────┬────────────────────────────────────┘
                     │ REST API (localhost:8000)
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Python FastAPI Backend                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ PDF Ingestion│  │  RAG Query   │  │ Vector Store │  │
│  │   Pipeline   │  │   Engine     │  │  (ChromaDB)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP API
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Ollama (Local LLM)                      │
│         qwen2.5:3b + nomic-embed-text                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

1. **Flutter SDK** (3.5.4+) - [Install Flutter](https://flutter.dev/docs/get-started/install)
2. **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
3. **Ollama** - [Install Ollama](https://ollama.ai)

### Step 1: Install Ollama Models

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

### Step 2: Setup Backend

```bash
cd backend_python

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python app/main.py
```

Backend will run at: **http://localhost:8000**

### Step 3: Setup Frontend

```bash
cd frontend_flutter

# Get dependencies
flutter pub get

# Run on Windows
flutter run -d windows

# Or macOS
flutter run -d macos

# Or Linux
flutter run -d linux
```

---

## 📖 Usage Guide

### 1. Upload Documents
- Navigate to **Documents** tab
- Click **Upload PDF**
- Select your study materials (textbooks, notes, etc.)
- Wait for processing (text extraction + embedding generation)

### 2. Ask Questions
- Go to **Chat** tab
- Type your question in natural language
- Get AI-powered answers with source references
- Continue the conversation for follow-up questions

### 3. Monitor System
- Check **Settings** tab for backend health
- View Ollama connection status
- See system information

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Flutter Desktop
- **UI**: Material 3 Design
- **State**: Provider
- **HTTP**: http package
- **Fonts**: Google Fonts (Inter)

### Backend
- **Framework**: FastAPI
- **LLM**: Ollama (qwen2.5:3b)
- **Embeddings**: nomic-embed-text
- **Vector DB**: ChromaDB
- **PDF**: PyPDF2

### Communication
- REST API over localhost
- JSON request/response format

---

## 📁 Project Structure

```
qnix-ai/
├── frontend_flutter/          # Flutter desktop app
│   ├── lib/
│   │   ├── main.dart         # Entry point
│   │   ├── app.dart          # Root widget
│   │   ├── core/             # Theme, constants
│   │   ├── features/         # Chat, Documents, Settings
│   │   ├── services/         # API service
│   │   └── widgets/          # Shared widgets
│   └── pubspec.yaml
│
├── backend_python/            # Python backend
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── api/              # Endpoints
│   │   ├── rag/              # RAG pipeline
│   │   ├── db/               # Vector store
│   │   └── utils/            # Utilities
│   └── requirements.txt
│
└── README.md                  # This file
```

---

## 🔧 Configuration

### Backend Configuration

Edit `backend_python/app/utils/ollama_client.py`:

```python
CHAT_MODEL = "qwen2.5:3b"          # Change LLM model
EMBEDDING_MODEL = "nomic-embed-text"  # Change embedding model
```

Edit `backend_python/app/rag/ingest.py`:

```python
CHUNK_SIZE = 1000      # Adjust chunk size
CHUNK_OVERLAP = 200    # Adjust overlap
```

### Frontend Configuration

Edit `frontend_flutter/lib/core/constants/api_constants.dart`:

```dart
static const String baseUrl = 'http://localhost:8000';  // Backend URL
```

---

## 🧪 Testing

### Test Backend Health

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
  -d '{"question": "What is the main topic?"}'
```

---

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.10+ is installed
- Check all dependencies are installed: `pip list`
- Verify Ollama is running: `ollama serve`

### Ollama connection failed
- Start Ollama: `ollama serve`
- Check models are installed: `ollama list`
- Verify port 11434 is not blocked

### Flutter build errors
- Run `flutter clean && flutter pub get`
- Ensure Flutter SDK is up to date: `flutter upgrade`
- Check desktop development is enabled: `flutter config --enable-windows-desktop`

### Documents not uploading
- Check PDF is not password-protected
- Ensure PDF contains text (not scanned images)
- Verify backend is running and accessible

---

## 🔮 Future Enhancements

- [ ] Document summarization
- [ ] MCQ generation for exam prep
- [ ] Sinhala language support
- [ ] Export chat history
- [ ] Advanced search filters
- [ ] Document annotations
- [ ] User authentication
- [ ] Cloud sync (optional)

---

## 📝 Development Notes

### Code Quality
- Production-ready code with comprehensive error handling
- Well-documented with inline comments
- Clean architecture with separation of concerns
- Type-safe with proper validation

### Performance
- Optimized chunking strategy for better retrieval
- Efficient vector similarity search
- Lazy loading for large document lists
- Smooth animations and transitions

### Scalability
- Easy to add new features
- Modular component structure
- Extensible API design
- Plugin-ready architecture

---

## 📄 License

MIT License - Free to use for educational purposes

---

## 🙏 Acknowledgments

- **Ollama** for local LLM serving
- **ChromaDB** for vector storage
- **Flutter** for cross-platform UI
- **FastAPI** for modern Python backend

---

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review backend/frontend README files
3. Ensure all prerequisites are installed
4. Verify Ollama models are downloaded

---

**Built with ❤️ for Sri Lankan Students**

*Empowering education through AI*
