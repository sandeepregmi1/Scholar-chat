# ScholarChat

ScholarChat is an advanced AI-powered study and research assistant designed to enhance the learning and research experience. It allows users to interact with their documents, generate study materials like flashcards and quizzes, take comprehensive notes, and conduct multi-document research, all through a modern, real-time web interface.

## 🚀 Features

- **Document Interaction**: Upload PDFs and text documents and chat directly with their contents using advanced Retrieval-Augmented Generation (RAG).
- **Multi-Document Chat**: Seamlessly query across multiple documents simultaneously for comprehensive research.
- **Smart Study Tools**:
  - Auto-generate **Flashcards** from your notes or documents.
  - Create interactive **Quizzes** to test your knowledge.
- **Advanced Note-Taking**: Integrated notebook application to organize your research and thoughts.
- **Citation Management**: Automatic tracking and formatting of citations for your research queries.
- **Real-Time Collaboration & Chat**: Lightning-fast, real-time communication powered by WebSockets.
- **Secure Authentication**: Robust user authentication and secure access to personal workspaces.

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite for rapid development and optimized builds
- **Routing**: React Router DOM (v7)
- **Styling**: Tailwind CSS / Custom CSS architecture
- **Networking**: Axios

### Backend
- **Framework**: FastAPI (Python 3.x)
- **Database**: PostgreSQL (via `psycopg2-binary`)
- **ORM & Migrations**: SQLAlchemy 2.0 & Alembic
- **Asynchronous Tasks**: Celery & Redis for background processing (document chunking, embeddings)
- **Real-Time**: WebSockets
- **Authentication**: JWT-based auth (Passlib, Bcrypt, Python-JOSE)

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx

## 📁 Project Structure

```
ScholarChat/
├── backend/                  # FastAPI Application
│   ├── alembic/              # Database migrations
│   ├── app/
│   │   ├── ai/               # LLM integration & prompts
│   │   ├── api/v1/           # REST & WebSocket routes
│   │   ├── core/             # Configuration & security
│   │   ├── db/               # Database connection
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── rag/              # Retrieval-Augmented Generation pipeline
│   │   ├── schemas/          # Pydantic validation models
│   │   ├── services/         # Business logic
│   │   ├── websocket/        # Real-time connection managers
│   │   └── workers/          # Celery background tasks
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React Application
│   ├── public/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components (Dashboard, Chat, etc.)
│   │   ├── routes/           # React Router configuration
│   │   ├── types/            # TypeScript interfaces
│   │   └── utils/            # Helper functions
│   └── package.json          # Node dependencies
├── docker/                   # Dockerfiles and scripts
├── nginx/                    # Nginx configuration
└── docker-compose.yml        # Multi-container orchestration
```

## 🏁 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- PostgreSQL
- Redis
- Docker & Docker Compose (optional, for containerized setup)

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ScholarChat.git
cd ScholarChat
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up your environment variables (create a .env file)
# Run database migrations
alembic upgrade head

# Start the FastAPI server
uvicorn app.main:app --reload
```

#### 3. Frontend Setup
```bash
cd ../frontend
npm install

# Start the Vite development server
npm run dev
```

#### 4. Background Workers (Celery)
To process documents and handle background tasks, start the Celery worker and Redis server:
```bash
# Ensure Redis is running locally
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

### Docker Deployment
To run the entire application stack using Docker Compose:
```bash
docker-compose up --build
```
This will spin up the FastAPI backend, React frontend, PostgreSQL database, Redis, Celery workers, and Nginx proxy.

## 📡 API Overview

The backend exposes several key RESTful endpoints (documented automatically via Swagger UI at `http://localhost:8000/docs`):

- **`/auth`**: User registration, login, and token management.
- **`/documents`**: Upload, process, and manage research documents.
- **`/chat`**: Single-document RAG chat queries.
- **`/multi-chat`**: Multi-document cross-reference queries.
- **`/ws-chat`**: WebSocket endpoints for streaming responses.
- **`/notes`, `/flashcards`, `/quiz`**: Study material generation and management.
- **`/citations`**: Retrieve generated citations for responses.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
