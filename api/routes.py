from collections.abc import Sequence
from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data import Note, NoteRepository, User, UserRepository, get_session

from .requests import NoteCreate, NotePatch, UserCreate
from .responses import NoteResponse, UserResponse


def setup_routes(
    app: FastAPI,
    note_repository: NoteRepository,
    user_repository: UserRepository,
) -> None:
    @app.get(path="/health", status_code=200)
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get(path="/hello", status_code=200)
    def hello() -> dict[str, str]:
        return {"message": "Hello from Notes API"}

    @app.get(path="/notes", status_code=200)
    def get_all_notes(
        session: Annotated[Session, Depends(get_session)],
    ) -> list[NoteResponse]:
        notes: Sequence[Note] = note_repository.get_all_notes(session=session)
        return [NoteResponse.from_orm(note) for note in notes]

    @app.post(path="/notes", status_code=201)
    def create_note(
        request: Annotated[NoteCreate, Body(description="Data to create a note")],
        session: Annotated[Session, Depends(get_session)],
    ) -> NoteResponse:
        # неплохо бы в сервис эту логику проверок вынести)
        user: User | None = user_repository.get_user(session=session, user_id=request.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        new_note: Note = note_repository.create_note(
            session=session,
            title=request.title,
            content=request.content,
            status=request.status,
            user_id=request.user_id,
        )
        session.commit()
        return NoteResponse.from_orm(new_note)

    @app.get(path="/notes/{note_id}", status_code=200)
    def get_note(
        note_id: Annotated[int, Path(description="Id of the note")],
        session: Annotated[Session, Depends(get_session)],
    ) -> NoteResponse:
        note: Note | None = note_repository.get_note(session=session, note_id=note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        return NoteResponse.from_orm(note)

    @app.head(path="/notes/{note_id}", status_code=200, response_class=Response)
    def head_note(
        note_id: Annotated[int, Path(description="Id of the note")],
        response: Response,
        session: Annotated[Session, Depends(get_session)],
    ) -> None:
        note: Note | None = note_repository.get_note(session=session, note_id=note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        response.headers["X-Note-Exists"] = "true"

    @app.patch(path="/notes/{note_id}", status_code=200)
    def patch_note(
        note_id: Annotated[int, Path(description="Id of the note")],
        request: Annotated[NotePatch, Body(description="Data to patch the note")],
        session: Annotated[Session, Depends(get_session)],
    ) -> NoteResponse:
        note: Note | None = note_repository.update_note(
            session=session,
            note_id=note_id,
            title=request.title,
            content=request.content,
            status=request.status,
        )
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        session.commit()

        return NoteResponse.from_orm(note)

    @app.delete(path="/notes/{note_id}", status_code=204)
    def delete_note(
        note_id: Annotated[int, Path(description="Id of the note")],
        session: Annotated[Session, Depends(get_session)],
    ) -> None:
        note_repository.delete_note(session=session, note_id=note_id)
        session.commit()

    @app.post(path="/users", status_code=201)
    def create_user(
        request: Annotated[UserCreate, Body(description="Data to create a user")],
        session: Annotated[Session, Depends(get_session)],
    ) -> UserResponse:
        try:
            new_user: User = user_repository.create_user(
                session=session,
                username=request.username,
                email=request.email,
            )
            session.commit()
        # можно свою проверку на уникальность email делать перед попыткой insert чтобы
        # вместо IntegrityError который прилет после неудачной попытки insert в бд,
        # ловить свою ошибку, но там тогда еще прийдется с конкурентностью поработать
        except IntegrityError as error:
            session.rollback()
            raise HTTPException(status_code=409, detail="Email already exists") from error

        return UserResponse.from_orm(new_user)

    @app.get(path="/users/{user_id}/notes", status_code=200)
    def get_user_notes(
        user_id: Annotated[int, Path(description="Id of the user")],
        session: Annotated[Session, Depends(get_session)],
    ) -> list[NoteResponse]:
        notes: Sequence[Note] = note_repository.get_all_notes_by_user_id(
            session=session,
            user_id=user_id,
        )
        return [NoteResponse.from_orm(note) for note in notes]
