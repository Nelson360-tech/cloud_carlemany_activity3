# Authentication & File Storage API

A REST API built with **FastAPI**, **PostgreSQL** and **Tortoise ORM**, following **hexagonal architecture** and **SOLID principles**. It provides user authentication (register, login, logout, token introspection) and file storage (CRUD, content upload, PDF merging), all with dependency injection and a relational database.

**Author:** Nelson Enrique Palacios Palacios
**Contact:** nelson0114@msn.com

---

## Features

### Authentication
- `POST /register` — Create a new user
- `POST /login` — Authenticate and obtain a session token
- `POST /logout` — Invalidate a session token
- `GET /introspect` — Verify a token and return the associated user

### Files
- `GET /files` — List all files owned by the authenticated user
- `POST /files` — Create a new file (metadata)
- `GET /files/{id}` — Retrieve file information and content
- `DELETE /files/{id}` — Delete a file
- `POST /files/{id}` — Upload file content
- `POST /files/merge` — Merge two PDF files

> All authenticated endpoints require the session token in a header named `Auth`.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| HTTP framework | FastAPI |
| ORM | Tortoise |
| Database | PostgreSQL |
| Migrations | Aerich |
| Dependency injection | `dependency-injector` |
| Password hashing | bcrypt |
| PDF handling | pypdf |
| Containerization | Docker + Docker Compose |

---

## Architecture

The project follows **hexagonal architecture** (ports and adapters). Each app (`authentication` and `files`) is structured as follows:

```text
app/<app_name>/
├── api/                     # FastAPI routers — HTTP layer only
├── domain/                  # Business logic
│   ├── controllers/         # Use case orchestration
│   ├── bos/                 # Business objects
│   ├── persistence/         # Persistence interfaces (ports)
│   └── exceptions/          # Domain-specific exceptions
├── dependency_injection/    # Container wiring API to domain to persistence
├── persistence/             # Concrete persistence implementations (adapters)
└── models.py                # Tortoise ORM models
```

This separation keeps business rules independent from both the HTTP framework and the database implementation, making each layer independently testable and swappable.

---

## Getting Started

### Prerequisites
- Docker and Docker Compose

### Run the project

```bash
git clone https://github.com/Nelson360-tech/cloud_carlemany_activity3.git
cd cloud_carlemany_activity3
docker-compose build
docker-compose up migrate
docker-compose up carlemany-backend
```

The API will be available at `http://localhost:8000/docs`.

### Environment variables

Copy `.env_example` to `.env` and adjust as needed:

```bash
cp .env_example .env
```

### Database migrations

```bash
docker-compose up make_migrations
docker-compose up migrate
```

---

## Example Usage

### Register a user

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"1234"}'
```

### Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"1234"}'
```

### Create a file

```bash
curl -X POST http://localhost:8000/files \
  -H "Auth: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filename":"document.pdf","description":"My file"}'
```

---

## License

This project is a personal portfolio project.