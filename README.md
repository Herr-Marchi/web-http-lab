# Web HTTP Lab

A small FastAPI Notes API for creating, reading, updating, and deleting notes over HTTP.

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
| HEAD | `/notes/{note_id}` | `200` with `X-Note-Exists: true` and no body; `404` if absent |
| PATCH | `/notes/{note_id}` | `200`, updated note; `404` if absent |
| DELETE | `/notes/{note_id}` | `204`, no body |

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

curl -I http://127.0.0.1:8000/notes/1
# HTTP/1.1 200 OK
# X-Note-Exists: true
# No response body

curl -X PATCH http://127.0.0.1:8000/notes/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Updated"}'
# {"id":1,"title":"Updated","content":"Request and response"}

curl -i -X DELETE http://127.0.0.1:8000/notes/1
# HTTP/1.1 204 No Content
# No response body

curl -i http://127.0.0.1:8000/notes/1
# HTTP/1.1 404 Not Found
# {"detail":"Note not found"}
```

`POST /notes` requires string `title` (1–80 characters) and `content` (1–500 characters). `PATCH /notes/{note_id}` accepts either field or both, with the same length limits. Invalid input returns `422`. A missing note on GET, HEAD, or PATCH returns `404`; GET and PATCH include `{"detail":"Note not found"}` in the JSON body. DELETE returns `204` even when the note is already absent.

## Limitations

Notes are stored only in the server process memory and disappear when the process restarts. The `.gitignore` excludes `.venv` and `.env`; keep secrets out of the repository.
