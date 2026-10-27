# Web HTTP Lab

A simple REST API built with Python and FastAPI.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Endpoints

- `GET /health` - Health check
- `GET /hello` - Welcome message
- `GET /notes` - Return a list of notes
- `POST /notes` - Create a new note and return it

API documentation: http://127.0.0.1:8000/docs