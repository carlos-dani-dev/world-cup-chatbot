# 🤖 Vue Chatbot Template

A full-stack, production-ready **chatbot template** built with **Vue 3** on the frontend and **FastAPI** on the backend. Designed to work with any **OpenAI-compatible API** — including local models via [Ollama](https://ollama.com/), cloud providers like OpenAI or Groq, and any self-hosted inference server that speaks the `/v1/chat/completions` protocol.

> **This is a template.** Clone it, configure your inference endpoint, and have a fully functional multi-user chatbot running in minutes.

---

## ✨ Features

- 💬 **Multi-session chat** — users can create, navigate, and continue multiple chat sessions
- 🔐 **JWT authentication** — access token + silent refresh via HttpOnly cookie
- 🧠 **Pluggable context strategies** — ships with a **Sliding Window** strategy; easily extendable
- 📝 **Markdown rendering** — bot responses rendered as rich Markdown with XSS sanitization
- 🗄️ **Persistent history** — all messages stored in PostgreSQL via SQLAlchemy
- 🐳 **Docker-first backend** — spin up Postgres, pgAdmin, and the FastAPI server with a single command
- ⚡ **Vite-powered frontend** — instant HMR, SVG component imports, TailwindCSS v4, and Vue DevTools

---

## 🏗️ Architecture Overview

```
vue-chatbot-template/
├── frontend/          # Vue 3 SPA (Vite + Pinia + Vue Router + TailwindCSS)
└── backend/           # FastAPI REST API (Python 3.13 + SQLAlchemy + Alembic)
```

### Request Flow

```
User types message
      │
      ▼
Vue 3 Frontend (Vite)
  ├─ Chat.vue          → sends POST /chats/{id}/messages
  ├─ Pinia stores      → caches sessions & messages locally
  └─ api.js            → handles JWT auth + silent token refresh
      │
      ▼
FastAPI Backend
  ├─ /auth             → login, signup, token refresh
  ├─ /chats            → CRUD for chat sessions
  └─ /chats/{id}/messages
      ├─ ChatService   → resolves context strategy (sliding window)
      ├─ InferenceGateway → wraps the HTTP call to the LLM
      └─ Persists user + assistant messages to PostgreSQL
      │
      ▼
OpenAI-Compatible LLM API
(Ollama, OpenAI, Groq, LM Studio, vLLM, etc.)
  POST /v1/chat/completions
```

---

## 🛠️ Tech Stack

### Frontend

| Tool | Versão | Purpose |
|---|---|---|
| [Vue 3](https://vuejs.org/) + `<script setup>` | ^3.5.38 | UI framework, Composition API |
| [Vite](https://vite.dev/) | ^8.0.16 | Dev server, bundler, HMR |
| [Pinia](https://pinia.vuejs.org/) | ^3.0.4 | State management (auth, sessions, messages) |
| [Vue Router](https://router.vuejs.org/) | ^5.1.0 | Client-side routing with navigation guards |
| [TailwindCSS](https://tailwindcss.com/) | ^4.3.1 | Utility-first styling |
| [Headless UI](https://headlessui.com/vue) | ^1.7.23 | Accessible animated sidebar drawer |
| [marked](https://marked.js.org/) | ^18.0.5 | Markdown rendering |
| [DOMPurify](https://github.com/cure53/DOMPurify) | ^3.4.11 | XSS sanitization |
| [vite-svg-loader](https://github.com/jpkleemans/vite-svg-loader) | ^5.1.1 | SVG files as Vue components |
| [Heroicons](https://heroicons.com/) | ^2.2.0 | Icon set |
| [@lottiefiles/dotlottie-vue](https://lottiefiles.com/) | ^0.11.16 | Lottie animations |
| [@preline/overlay](https://preline.co/) | ^4.2.0 | Overlay components |

### Backend

| Tool | Versão | Purpose |
|---|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | >=0.136.3,<0.137.0 | REST API framework |
| [Python](https://www.python.org/) | >=3.13,<4.0 | Runtime |
| [SQLAlchemy](https://www.sqlalchemy.org/) | >=2.0.50,<3.0.0 | ORM with typed `Mapped` columns |
| [Alembic](https://alembic.sqlalchemy.org/) | >=1.18.4,<2.0.0 | Database migrations |
| [PostgreSQL](https://www.postgresql.org/) | 18-alpine | Primary database (via Docker) |
| [python-jose](https://python-jose.readthedocs.io/) | >=3.5.0,<4.0.0 | JWT encoding/decoding |
| [bcrypt](https://pypi.org/project/bcrypt/) | >=5.0.0,<6.0.0 | Password hashing |
| [httpx](https://www.python-httpx.org/) | >=0.28.1,<0.29.0 | HTTP client for inference API calls |
| [Poetry](https://python-poetry.org/) | >=2.0.0,<3.0.0 | Dependency management |
| [Docker + Docker Compose](https://docs.docker.com/compose/) | - | Containerized backend stack |
| [pgAdmin 4](https://www.pgadmin.org/) | latest | Database management UI |
| [Pandas](https://pandas.pydata.org/) | >=3.0.3,<4.0.0 | Data manipulation |
| [NumPy](https://numpy.org/) | >=2.4.6,<3.0.0 | Numerical computing |
| [Taskipy](https://github.com/taskipy/taskipy) | >=1.14.1,<2.0.0 | Task runner |
| [Starlette](https://www.starlette.io/) | >=1.2.1,<2.0.0 | ASGI toolkit |

---

## 🚀 Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) `^22.18.0` or `>=24.12.0`
- [Python](https://www.python.org/) `>=3.13`
- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/docs/#installation)
- A running **OpenAI-compatible LLM API** (see [Inference Setup](#-inference-setup))

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/vue-chatbot-template.git
cd vue-chatbot-template
```

---

### 2. Backend — Docker Compose

#### 2a. Configure environment variables

```bash
cd backend
cp .env .env.local   # keep .env as a reference; edit .env directly for local use
```

Edit `.env` with your settings:

```env
# --- Database ---
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
DB_NAME=chatbot-db
PG_DATA=/var/lib/postgresql/data

SQLALCHEMY_DATABASE_URL=postgresql://postgres:your_secure_password@postgres:5432/chatbot-db

# --- pgAdmin ---
PGADMIN4_EMAIL=admin@admin.com
PGADMIN4_PASSWORD=your_pgadmin_password

# --- JWT ---
SECRET_KEY=your_secret_key_here          # generate with: openssl rand -base64 32
ALGORITHM=HS256

# --- Chat behavior ---
CHAT_DEFAULT_SYSTEM_PROMPT="You are a helpful assistant."
CHAT_MAX_CONTENT_CHARS=100000
CHAT_MAX_MESSAGES=20

# --- Inference API (OpenAI-compatible) ---
INFERENCE_BASE_URL=http://host.docker.internal:11434   # Use host.docker.internal for local Ollama
INFERENCE_API_KEY=ollama                    # Not required for local Ollama

# --- Context Strategy ---
CONTEXT_STRATEGY=sliding_window
WINDOW_SIZE=3   # number of past messages sent as context to the LLM
```

#### 2b. Start the stack

```bash
docker compose up --build
```

This starts three containers:

| Container | Port | Description |
|---|---|---|
| `wc_chatbot_postgres` | `5432` | PostgreSQL database |
| `wc_chatbot_pgadmin4` | `5050` | pgAdmin 4 web UI |
| `wc_chatbot_api` | `8000` | FastAPI application |

| URL | Description |
|---|---|
| http://localhost:8000 | REST API |
| http://localhost:8000/docs | Swagger interactive docs |
| http://localhost:5050 | pgAdmin 4 |

> **Taskipy shortcuts** (run from inside `backend/`):
> ```bash
> poetry run task run     # docker compose up --build
> poetry run task clean   # docker compose down -v
> poetry run task test    # pytest
> ```

#### 2c. Database migrations (optional)

Tables are auto-created on startup. To run Alembic migrations manually:

```bash
cd backend
poetry run alembic upgrade head
```

---

### 3. Frontend — Vite Dev Server

```bash
cd frontend
npm install
npm run dev
```

The app will be available at **http://localhost:5173**.

> The frontend calls the backend directly at `http://localhost:8000`. Ensure the backend is running before using the app.

---

## 🧠 Inference Setup

The backend calls any endpoint implementing the **OpenAI `/v1/chat/completions`** protocol. Set `INFERENCE_BASE_URL` and `INFERENCE_API_KEY` in `.env`.

### Option A — Ollama (local, free)

> **⚠️ Important for Linux / Docker users:** By default, Ollama only listens to `localhost` (127.0.0.1). For the Dockerized backend to reach Ollama on your host machine, you must configure Ollama to listen on all network interfaces (`0.0.0.0`):
> 
> ```bash
> sudo mkdir -p /etc/systemd/system/ollama.service.d
> echo -e "[Service]\nEnvironment=\"OLLAMA_HOST=0.0.0.0\"" | sudo tee /etc/systemd/system/ollama.service.d/override.conf
> sudo systemctl daemon-reload
> sudo systemctl restart ollama
> ```

```bash
# Install Ollama: https://ollama.com
ollama pull llama3.2:3b
```

In your backend `.env`, make sure to use `host.docker.internal` instead of `localhost`:

```env
INFERENCE_BASE_URL=http://host.docker.internal:11434
INFERENCE_API_KEY=ollama
```

Set the model in `frontend/src/views/Chat.vue`:

```js
const model = "llama3.2:3b";
```

### Option B — OpenAI

```env
INFERENCE_BASE_URL=https://api.openai.com
INFERENCE_API_KEY=sk-...
```

```js
const model = "gpt-4o-mini";
```

### Option C — Groq

```env
INFERENCE_BASE_URL=https://api.groq.com/openai
INFERENCE_API_KEY=gsk_...
```

```js
const model = "llama-3.1-8b-instant";
```

Any provider serving `POST /v1/chat/completions` will work (LM Studio, vLLM, Together AI, etc.).

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── views/                   # Routed pages
│   │   ├── Chat.vue             # Main chat interface
│   │   ├── Login.vue            # Sign in page
│   │   └── Signup.vue           # Registration page
│   ├── components/              # Reusable UI components
│   │   ├── SideBarMenu.vue      # Slide-over session drawer (Headless UI)
│   │   ├── ProfileMenu.vue      # Profile dropdown (sign out)
│   │   └── Message.vue          # Individual chat message bubble
│   ├── stores/                  # Pinia state management
│   │   └── auth.js              # Access token + localStorage persistence
│   ├── services/                # API communication layer
│   │   └── api.js               # Base fetch + JWT silent refresh interceptor
│   ├── router/
│   │   └── router.js            # Routes + auth navigation guard
│   └── assets/
│       ├── main.css             # Global styles
│       └── icons/               # SVG icons
├── package.json                 # Dependencies and scripts
├── vite.config.js               # Vite configuration
├── dockerfile                   # Frontend Docker image
└── index.html                   # Entry HTML

backend/
├── src/
│   ├── app.py                   # FastAPI app, CORS, router registration
│   ├── config.py                # Environment variable loading
│   ├── models.py                # SQLAlchemy ORM models (User, ChatSession, ChatMessage)
│   ├── database.py              # Engine + SessionLocal factory
│   ├── dependencies.py          # FastAPI DI (db session, auth, services)
│   ├── routes/
│   │   ├── user_route.py        # /auth — login, signup, token refresh
│   │   ├── chat_route.py        # /chats — session CRUD
│   │   └── message_route.py     # /chats/{id}/messages — send & list messages
│   ├── services/
│   │   ├── chat_service.py      # Core logic: context strategy, prompt building, persistence
│   │   └── user_service.py      # Auth, JWT creation, password hashing
│   ├── clients/
│   │   ├── inference_client.py  # httpx client for the OpenAI-compatible LLM API
│   │   └── inference_gw.py      # Gateway wrapper
│   ├── repository/              # Database access layer (repositories pattern)
│   │   ├── chat_session_repository.py
│   │   └── user_repository.py
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── user_schema.py
│   │   ├── chat_session_schema.py
│   │   ├── chat_message_schema.py
│   │   └── openaiLike_schema.py # OpenAI-compatible request/response schemas
│   └── exceptions/              # Custom exception types
│       └── exceptions.py
├── alembic/                     # Database migrations
├── alembic.ini                  # Alembic configuration
├── pyproject.toml               # Poetry dependencies
├── poetry.lock                  # Dependency lock file
├── dockerfile                   # Backend Docker image
└── .env                         # Environment variables

docker-compose.yml              # Full stack orchestration
```

---

## ⚙️ Context Strategy

The backend controls how much conversation history is forwarded to the LLM on each request. The active strategy is set via the `CONTEXT_STRATEGY` environment variable.

| Strategy | `CONTEXT_STRATEGY` value | Description |
|---|---|---|
| **Sliding Window** | `sliding_window` | Sends the last `WINDOW_SIZE` messages as context |

To add a new strategy, implement the `ContextStrategy` protocol in `chat_service.py` and register it in the `STRATEGIES` dict:

```python
class MySummaryStrategy:
    def build(self, messages, *, system_prompt="", conversation_summary=None):
        # your logic here
        return ContextResult(messages=..., window_size=...)

STRATEGIES = {
    "sliding_window": SlidingWindowStrategy,
    "my_summary": MySummaryStrategy,   # ← add here
}
```

Then set `CONTEXT_STRATEGY=my_summary` in `.env`.

---

## 🔐 Authentication Flow

```
POST /auth/          →  create account
POST /auth/token     →  login → returns { access_token } + sets HttpOnly refresh_token cookie
POST /auth/refresh   →  silently renews access_token using the cookie
GET /auth/           →  get current user info
```

The frontend (`api.js`) automatically retries any `401` response by hitting `/auth/refresh` before re-sending the original request. Users stay logged in transparently until the refresh token expires (5 days by default).

### JWT Configuration

- **Access Token**: 20 minutes expiration
- **Refresh Token**: 5 days expiration (stored as HttpOnly cookie)
- **Algorithm**: HS256
- **Storage**: Access token in localStorage, refresh token in HttpOnly cookie

---

## 🗄️ Database Schema

### Tables

**users**
- `id` (UUID, PK)
- `email` (String)
- `username` (String)
- `hashed_password` (String)
- `role` (String)
- Relationship: One-to-many with `chat_sessions`

**chat_sessions**
- `id` (UUID, PK)
- `user_id` (UUID, FK → users.id)
- `title` (String)
- `channel` (String, default: "web")
- `created_at` (DateTime)
- `chat_session_summary` (String, nullable)
- `session_metadata` (JSON)
- Relationships: Many-to-one with `users`, One-to-many with `chat_messages`

**chat_messages**
- `id` (UUID, PK)
- `session_id` (UUID, FK → chat_sessions.id, ON DELETE CASCADE)
- `role` (String: "user" | "assistant" | "system")
- `content` (String)
- `created_at` (DateTime)
- Relationship: Many-to-one with `chat_sessions`

## 🚨 Custom Exceptions

The backend implements custom exception types for better error handling:

- `UsernameAlreadyExistsError`: Raised when attempting to create a user with an existing username
- `ChatSessionNotFoundError`: Raised when a requested chat session doesn't exist or doesn't belong to the user
- `InferenceConnectionError`: Raised when unable to connect to the inference API
- `InferenceHTTPError`: Raised when the inference API returns an HTTP error (4xx/5xx)
- `InferenceParseError`: Raised when unable to parse the inference API response as JSON

## 🧪 Running Tests

```bash
cd backend
poetry run task test
# or directly:
poetry run pytest
```

## 📊 API Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth` | Create new user account | No |
| POST | `/auth/token` | Login (returns access token + sets refresh cookie) | No |
| POST | `/auth/refresh` | Refresh access token using refresh cookie | No |
| GET | `/auth` | Get current user info | Yes |

### Chat Sessions (`/chats`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/chats` | List all chat sessions for current user | Yes |
| GET | `/chats/{id}` | Get specific chat session details | Yes |
| POST | `/chats` | Create new chat session | Yes |
| DELETE | `/chats/{id}` | Delete chat session | Yes |

### Messages (`/chats/{id}/messages`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/chats/{id}/messages` | List all messages in a chat session | Yes |
| POST | `/chats/{id}/messages` | Send message and get LLM response | Yes |

### Health Check

| Method | Endpoint | Description |
|---|---|---|
| GET | `/healthy` | API health check |

---

## 🔧 Customization Tips

| What | How |
|---|---|
| Change the default system prompt | Set `CHAT_DEFAULT_SYSTEM_PROMPT` in `.env` |
| Override system prompt per request | Pass `system_prompt` in `POST /chats/{id}/messages` body |
| Change the LLM model | Update the `model` constant in `frontend/src/views/Chat.vue` |
| Make model configurable via env | Use `const model = import.meta.env.VITE_MODEL ?? "llama3.2:3b"` |
| Add streaming responses | Extend `InferenceHttpClient` to handle SSE; `ChatCompletionRequest` already has a `stream` field |
| Add a new context strategy | Implement `ContextStrategy` protocol and register in `STRATEGIES` |
| Add i18n | Drop in [vue-i18n](https://vue-i18n.intlify.dev/) and replace hardcoded strings |

---

## 👨‍💻 Development Team

**Developer**: Carlos Daniel Rocha
**Contact**: carlos.rocha@ufpi.edu.br

## 📄 License

MIT — use freely, modify as needed.

## 🚀 Roadmap / Próximos Passos

- [ ] Implement streaming responses (SSE) for real-time LLM output
- [ ] Add more context strategies (summary-based, semantic search)
- [ ] Implement file upload and document analysis capabilities
- [ ] Add internationalization (i18n) support
- [ ] Implement rate limiting for API endpoints
- [ ] Add comprehensive test coverage for frontend and backend
- [ ] Implement WebSocket support for real-time chat updates
- [ ] Add admin panel for user and session management
- [ ] Implement conversation export functionality (PDF, Markdown)
- [ ] Add analytics and usage metrics dashboard
- [ ] Implement multi-language model support per session
- [ ] Add conversation sharing and collaboration features
