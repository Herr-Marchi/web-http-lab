from typing import Annotated

from fastapi import FastAPI, Body, Path, HTTPException, Response
from pydantic import BaseModel, Field

app: FastAPI = FastAPI(title="Notes API", version="0.1.0")


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)


class NotePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=80)
    content: str | None = Field(default=None, min_length=1, max_length=500)


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
    request: Annotated[NoteCreate, Body(description="Data to create a note")],
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


@app.get(path="/notes/{note_id}", status_code=200)
def get_note(
    note_id: Annotated[int, Path(description="Id of the note")],
) -> dict[str, str | int]:
    for note in notes:
        if note["id"] == note_id:
            return note

    raise HTTPException(status_code=404, detail="Note not found")


@app.head(path="/notes/{note_id}", status_code=200, response_class=Response)
def head_note(
    note_id: Annotated[int, Path(description="Id of the note")],
    response: Response,
) -> None:
    for note in notes:
        if note["id"] == note_id:
            response.headers["X-Note-Exists"] = "true"
            return

    response.status_code = 404


@app.patch(path="/notes/{note_id}", status_code=200)
def patch_note(
    note_id: Annotated[int, Path(description="Id of the note")],
    request: Annotated[NotePatch, Body(description="Data to patch the note")],
) -> dict[str, str | int]:
    note_to_patch: dict[str, str | int] | None = next(
        (
            note
            for note in notes
            if note["id"] == note_id
        ),
        None,
    )
    if note_to_patch is None:
        raise HTTPException(status_code=404, detail="Note not found")

    if request.title is not None:
        note_to_patch["title"] = request.title
    if request.content is not None:
        note_to_patch["content"] = request.content

    return note_to_patch


@app.delete(path="/notes/{note_id}", status_code=204)
def delete_note(
    note_id: Annotated[int, Path(description="Id of the note")],
) -> None:
    index_to_delete: int | None = next(
        (
            i
            for i, note in enumerate(notes)
            if note["id"] == note_id
        ),
        None,
    )
    if index_to_delete is not None:
        notes.pop(index_to_delete)
