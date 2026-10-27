from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app: FastAPI = FastAPI(title="Notes API", version="0.1.0")


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)


notes: list[dict[str, str | int]] = []
next_id: int = 1


@app.get(path="/health", status_code=200)
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(path="/hello", status_code=200)
def hello() -> dict[str, str]:
    return {"message": "Hello from Notes API"}


@app.get(path="/notes", status_code=200)
def get_all_notes() -> list[dict[str, str | int]]:
    return notes


@app.post(path="/notes", status_code=201)
def create_note(
    request: Annotated[NoteCreate, Body(description="Data to create a note")]
) -> dict[str, str | int]:
    global next_id

    new_note: dict[str, str | int] = {
        "id": next_id,
        "title": request.title,
        "content": request.content,
    }
    notes.append(new_note)
    next_id += 1
    return new_note
