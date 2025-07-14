# Shelf API

Shelf is a modular and extensible backend application for organizing and managing vinyl record collections. Built with FastAPI, SQLAlchemy, and Alembic, the project uses a modern `src/`-oriented architecture, following clean code practices and containerized with Docker.

## ✨ Features

* **User album management**: Add, remove, and update albums in your collection
* **Storage system modeling**: Define shelves, slots, and groups to physically represent your collection
* **Detailed record info**: Support for albums, releases, mediums, and works
* **PostgreSQL database**: Structured relational schema
* **Alembic migrations**: Easy schema evolution
* **Pydantic models**: Type-checked schemas for requests and responses
* **Logging**: Configured and extendable
* **Testable**: Pytest-ready setup

---

## 🚀 Quick Start

### Development

```bash
# Clone the repository
$ git clone https://github.com/your-username/shelf.git
$ cd shelf

# Build and start containers
$ poe run

# Apply migrations
$ poe migrate

# Check logs
$ poe logs
```

### API Access

The API is available at: `http://localhost:8000` by default.

Swagger UI docs are accessible at: `http://localhost:8000/docs`

---

## 📂 Project Structure

```bash
src/
 ├── shelf/
     ├── app/
     │    ├── core/           # Config and constants
     │    ├── db/             # Session and DB logic
     │    ├── models/         # SQLAlchemy models
     │    ├── schemas/        # Pydantic schemas
     │    ├── crud/           # Database access logic
     │    ├── routers/        # FastAPI route handlers
     │    └── main.py         # Entry point

alembic/                     # Migration files
pyproject.toml               # Project config (Poetry + Ruff + Poe)
```

---

## 🤧 Tech Stack

* **FastAPI** for API development
* **SQLAlchemy 2.0** ORM with modern typed syntax
* **Alembic** for database migrations
* **Pydantic v2** for request/response models
* **PostgreSQL** as the database
* **Docker + Compose** for container orchestration
* **Poetry** for dependency management
* **Poe the Poet** for task running
* **Ruff** for linting

---

## 📃 Example Endpoints

```http
GET /albums/                # List albums
POST /albums/               # Add album
PATCH /albums/{id}          # Update album
DELETE /albums/{id}         # Remove album

GET /storage_item/         # View storage items
POST /storage_group/       # Create new group
```

---

## 🌐 Environment Variables

```env
POSTGRES_USER=shelf_user
POSTGRES_PASSWORD=shelf
POSTGRES_DB=shelf_db
POSTGRES_HOST=postgresql
POSTGRES_PORT=5432
```

---

## ✅ Tasks

All development commands are managed with **Poe the Poet**:

```bash
poe run            # Build & start dev server
poe makemigrations # Create new migration
poe migrate        # Apply migrations
poe test           # Run tests
poe logs           # Tail docker logs
```

---

## 🚫 License

MIT License. See `LICENSE` for details.

---

Made with ❤️ by Slava.
