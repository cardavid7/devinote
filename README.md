<div align="center">

# 📝 Devinote API

**A collaborative notes REST API built with FastAPI, SQLModel and PostgreSQL.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.38-ff6b6b?style=flat-square)](https://sqlmodel.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.18-blue?style=flat-square)](https://alembic.sqlalchemy.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📖 Overview

**Devinote** is a RESTful API that allows users to create, organize, and collaborate on notes. It features JWT-based authentication, label organization, and a granular sharing system with role-based permissions (`read` / `edit`).

### ✨ Key Features

- 🔐 **JWT Authentication** — Secure token-based auth with OAuth2 password flow
- 📝 **Notes Management** — Create, update, delete, and list notes with color support
- 🏷️ **Labels** — Organize notes with custom labels (unique per user)
- 🤝 **Sharing System** — Share notes and labels with other users, with `read` or `edit` roles
- 🗄️ **PostgreSQL** — Production-ready database with Alembic migrations
- 🚀 **Render / Railway** — Ready to deploy

---

## 🏗️ Architecture

```
devinote/
├── app/
│   ├── api/
│   │   ├── deps.py              # Shared dependencies (DB session, current user)
│   │   └── routers/
│   │       ├── auth_router.py   # Register, login, token
│   │       ├── notes_router.py  # CRUD notes
│   │       ├── labels_router.py # CRUD labels
│   │       └── shares_router.py # Share notes & labels
│   ├── core/
│   │   ├── config.py            # Settings via pydantic-settings
│   │   └── db.py                # Engine & session factory
│   ├── models/
│   │   ├── user.py              # User ORM + schemas
│   │   ├── note.py              # Note ORM + schemas
│   │   ├── label.py             # Label + NoteLabelLink ORM
│   │   └── share.py             # NoteShare + LabelShare ORM
│   ├── repositories/            # Data access layer
│   ├── services/                # Business logic layer
│   └── main.py                  # App factory & middleware
├── alembic/                     # Database migrations
├── Procfile                     # Render / Railway start command
├── requirements.txt
└── .env.example
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 14+

### 1. Clone the repository

```bash
git clone https://github.com/your-username/devinote.git
cd devinote
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/devinote
JWT_SECRET_KEY=your-super-secret-key   # generate: python -c "import secrets; print(secrets.token_hex(32))"
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=DEV
ALLOWED_ORIGINS=*
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the development server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive documentation at `http://localhost:8000/docs`.

---

## 📡 API Reference

All endpoints are prefixed with `/api/v1`.

### 🔐 Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | ❌ | Register a new user |
| `POST` | `/auth/login` | ❌ | Login with email & password → returns JWT |
| `POST` | `/auth/token` | ❌ | OAuth2 password flow (Swagger compatible) |

#### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "strongpassword"
}
```

#### Login
```http
POST /api/v1/auth/login?email=user@example.com&password=strongpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 📝 Notes

> All notes endpoints require `Authorization: Bearer <token>`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/notes/` | List all visible notes (owned + shared) |
| `POST` | `/notes/` | Create a new note |
| `PATCH` | `/notes/{note_id}` | Update a note |
| `DELETE` | `/notes/{note_id}` | Delete a note |

#### Create a Note
```http
POST /api/v1/notes/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My first note",
  "content": "Hello, Devinote!",
  "color": "#f0e68c",
  "label_ids": [1, 2]
}
```

#### Update a Note
```http
PATCH /api/v1/notes/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated title",
  "color": "#add8e6"
}
```

---

### 🏷️ Labels

> All labels endpoints require `Authorization: Bearer <token>`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/labels/` | List user's labels |
| `POST` | `/labels/` | Create a new label |
| `DELETE` | `/labels/{label_id}` | Delete a label |

#### Create a Label
```http
POST /api/v1/labels/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Work"
}
```

---

### 🤝 Shares

> All shares endpoints require `Authorization: Bearer <token>`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/shares/notes/{note_id}` | Share a note with a user |
| `DELETE` | `/shares/notes/{note_id}` | Revoke note access |
| `POST` | `/shares/labels/{label_id}` | Share a label with a user |
| `DELETE` | `/shares/labels/{label_id}` | Revoke label access |

#### Share a Note
```http
POST /api/v1/shares/notes/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "target_user_id": 2,
  "role": "edit"
}
```

**Roles:**
| Role | Permissions |
|------|-------------|
| `read` | View the note/label |
| `edit` | View and modify the note/label |

---

## 🗃️ Data Models

```
User
 ├── id, email (unique), full_name, hashed_password, active
 │
 ├── Note (owner_id → User.id)
 │    ├── id, title, content, color
 │    ├── NoteLabelLink (note_id, label_id)   ← many-to-many
 │    └── NoteShare (note_id, user_id, role)  ← sharing
 │
 └── Label (owner_id → User.id)
      ├── id, name  [unique per owner]
      └── LabelShare (label_id, user_id, role) ← sharing
```

---

## 🌐 Deployment

### Render

1. Create a **PostgreSQL** database on Render and copy the *Internal Database URL*.
2. Change the URL prefix from `postgresql://` to `postgresql+psycopg://`.
3. Create a **Web Service** from your GitHub repo with:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set the environment variables in the *Environment* tab.

### Railway

1. Create a new project and import your GitHub repository.
2. Add a **PostgreSQL** plugin — Railway auto-injects `DATABASE_URL`.
3. Set the remaining environment variables.
4. Railway picks up the `Procfile` automatically.

### Environment Variables (production)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | `postgresql+psycopg://user:pass@host:5432/db` |
| `JWT_SECRET_KEY` | Random 32-byte hex string |
| `JWT_ALGORITHM` | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL in minutes |
| `ENVIRONMENT` | `PROD` |
| `ALLOWED_ORIGINS` | Comma-separated frontend URLs |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM | [SQLModel](https://sqlmodel.tiangolo.com/) |
| Database | [PostgreSQL](https://www.postgresql.org/) |
| DB Driver | [psycopg 3](https://www.psycopg.org/) |
| Migrations | [Alembic](https://alembic.sqlalchemy.org/) |
| Auth | [PyJWT](https://pyjwt.readthedocs.io/) |
| Password Hashing | [pwdlib (argon2)](https://pwdlib.readthedocs.io/) |
| Validation | [Pydantic v2](https://docs.pydantic.dev/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
