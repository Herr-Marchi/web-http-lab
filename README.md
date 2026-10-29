# Web HTTP Lab

A small FastAPI Notes API. Notes are stored in PostgreSQL and survive an API restart.

## Requirements

Python 3.14 or newer and access to PostgreSQL. Docker is needed for the container examples below.

## Setup and run

Create and activate a virtual environment from the project directory:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Copy `example.env` to `.env`:

```bash
cp example.env .env
```

Set `DATABASE_URL` in `.env` for the PostgreSQL database you want to use.

### Existing PostgreSQL database

If you already have a PostgreSQL database, including a remote one, put its host, port, database name, username, and password into the connection URL in `.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME
```

Replace the uppercase placeholders with your database's actual connection details.

### Local PostgreSQL with Docker

To start a local database, run PostgreSQL with a persistent Docker volume:

```bash
docker run --name notes-db -e POSTGRES_USER=notes -e POSTGRES_PASSWORD=notes \
  -e POSTGRES_DB=notes -p 127.0.0.1:55432:5432 -v notes_pgdata:/var/lib/postgresql/data \
  -d postgres:16-alpine
```

For this local container, set the following URL in `.env`:

```dotenv
DATABASE_URL=postgresql+psycopg://notes:notes@localhost:55432/notes
```

With either database, apply the migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive documentation is at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Run API and PostgreSQL with Docker Compose

```bash
docker compose up -d --build
docker compose exec api alembic upgrade head
```

Compose starts the API and PostgreSQL together. The database uses a named volume, so its data survives container recreation.

## Schema

Alembic migrations create the tables. The SQL below describes the resulting schema; it is not an additional setup command. The first migration creates `notes`, and the second creates `users` and adds the foreign key.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    content VARCHAR(500) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    status VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE INDEX ix_notes_user_id ON notes (user_id);
```

## Endpoints

| Method | Path | Response |
| --- | --- | --- |
| GET | `/health` | `200`, `{"status":"ok"}` |
| GET | `/hello` | `200`, `{"message":"Hello from Notes API"}` |
| POST | `/users` | `201`, created user; `409` if email already exists |
| GET | `/users/{user_id}/notes` | `200`, notes filtered by `user_id` |
| GET | `/notes` | `200`, list of notes |
| POST | `/notes` | `201`, created note; `404` if `user_id` does not exist |
| GET | `/notes/{note_id}` | `200`, matching note; `404` if absent |
| HEAD | `/notes/{note_id}` | `200` with `X-Note-Exists: true` and no body; `404` if absent |
| PATCH | `/notes/{note_id}` | `200`, updated note; `404` if absent |
| DELETE | `/notes/{note_id}` | `204`, no body, including when absent |

Example requests and responses, assuming a fresh database:

```bash
curl -i -X POST http://127.0.0.1:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","email":"demo@example.invalid"}'
# HTTP/1.1 201 Created
# {"id":1,"username":"demo","email":"demo@example.invalid"}

curl http://127.0.0.1:8000/notes
# []

curl -i -X POST http://127.0.0.1:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"HTTP","content":"Request and response","status":"new","user_id":1}'
# HTTP/1.1 201 Created
# {"id":1,"title":"HTTP","content":"Request and response","status":"new","created_at":"2026-10-28T12:00:00+00:00","user_id":1}

curl http://127.0.0.1:8000/notes/1
# {"id":1,"title":"HTTP","content":"Request and response","status":"new","created_at":"2026-10-28T12:00:00+00:00","user_id":1}

curl -I http://127.0.0.1:8000/notes/1
# HTTP/1.1 200 OK
# X-Note-Exists: true
# No response body

curl -X PATCH http://127.0.0.1:8000/notes/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Updated","status":"done"}'
# {"id":1,"title":"Updated","content":"Request and response","status":"done","created_at":"2026-10-28T12:00:00+00:00","user_id":1}

curl -i -X DELETE http://127.0.0.1:8000/notes/1
# HTTP/1.1 204 No Content
# No response body

curl -i http://127.0.0.1:8000/notes/1
# HTTP/1.1 404 Not Found
# {"detail":"Note not found"}
```

## Current limitations

The API has no authentication or ownership checks. Clients supply `user_id` when creating notes, and any caller can read, update, or delete a note by its ID.

The layers are not fully separated yet: route handlers use SQLAlchemy sessions and ORM models directly, apply business rules such as checking that a user exists before creating a note, and commit transactions.

When running with Compose, database migrations still need to be applied separately. Running without Compose requires configuring and starting the API and PostgreSQL separately.

Project requirements are currently split between this README, which specifies the Python version, and `requirements.txt`, which lists third-party packages. A `pyproject.toml` could declare the supported Python version and package dependencies together.
