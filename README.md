# Web HTTP Lab

A small FastAPI Notes API for creating and reading notes over HTTP.

## Requirements

Python 3.10 or newer.

## Setup and run

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with `.venv\Scripts\activate` instead.

Install dependencies and start the server:

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Endpoints

| Method | Path | Success response |
| --- | --- | --- |
| GET | `/health` | `200`, `{"status":"ok"}` |
| GET | `/hello` | `200`, `{"message":"Hello from Notes API"}` |
| GET | `/notes` | `200`, list of notes (`[]` initially) |
| POST | `/notes` | `201`, created note with an `id` |
| GET | `/notes/{note_id}` | `200`, matching note; `404` if absent |

Example requests and responses (starting with an empty notes list):

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}

curl http://127.0.0.1:8000/hello
# {"message":"Hello from Notes API"}

curl http://127.0.0.1:8000/notes
# []

curl -i -X POST http://127.0.0.1:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"HTTP","content":"Request and response"}'
# HTTP/1.1 201 Created
# {"id":1,"title":"HTTP","content":"Request and response"}

curl http://127.0.0.1:8000/notes/1
# {"id":1,"title":"HTTP","content":"Request and response"}
```

`POST /notes` requires string `title` (1–80 characters) and `content` (1–500 characters). Invalid input returns `422`. A missing note returns `404` with `{"detail":"Note not found"}`.

## Limitations

Notes are stored only in the server process memory and disappear when the process restarts. The `.gitignore` excludes `.venv` and `.env`; keep secrets out of the repository.
