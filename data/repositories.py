from collections.abc import Sequence

from sqlalchemy import Delete, ScalarResult, Select, delete, select
from sqlalchemy.orm import Session

from .models import Note, User

"""Cделаю репозиторий как набор статик методов, закрытие транзакции и ролбек
делегирую во вне, для того чтобы в пределах одной транзакции можно было
несколько методов репозитория вызвать передавая одну и ту же сессию.
Альтернативно можно сделать uow для изоляции этой работы, заодно эндпоинты чище станут,
потому что работа с персистом уйдет из них, но пока маловат проект для этого
"""
class NoteRepository:
    @staticmethod
    def get_note(session: Session, note_id: int) -> Note | None:
        statement: Select[Note] = (
            select(Note)
            .where(Note.id == note_id)
        )
        scalar_result: ScalarResult[Note] = session.scalars(statement)
        return scalar_result.one_or_none()

    @staticmethod
    def get_all_notes(session: Session) -> Sequence[Note]:
        statement: Select[Note] = select(Note)
        scalar_result: ScalarResult[Note] = session.scalars(statement)
        return scalar_result.all()

    @staticmethod
    def get_all_notes_by_user_id(session: Session, user_id: int) -> Sequence[Note]:
        statement: Select[Note] = (
            select(Note)
            .where(Note.user_id == user_id)
        )
        scalar_result: ScalarResult[Note] = session.scalars(statement)
        return scalar_result.all()

    # не хочу напрямую передавать NoteCreate чтобы не нарушать направления зависимостей
    @staticmethod
    def create_note(
        session: Session,
        title: str,
        content: str,
        status: str,
        user_id: int,
    ) -> Note:
        new_note: Note = Note(
            title=title,
            content=content,
            status=status,
            user_id=user_id,
        )
        session.add(new_note)
        # отправляю insert уже сейчас, чтобы получить айди, но не фиксирую транзакцию комитом
        session.flush()
        return new_note

    @staticmethod
    def delete_note(session: Session, note_id: int) -> None:
        statement: Delete = (
            delete(Note)
            .where(Note.id == note_id)
        )
        session.execute(statement)

    @staticmethod
    def update_note(
        session: Session,
        note_id: int,
        title: str | None = None,
        content: str | None = None,
        status: str | None = None,
    ) -> Note | None:
        statement: Select[Note] = (
            select(Note)
            .where(Note.id == note_id)
        )
        scalar_result: ScalarResult[Note] = session.scalars(statement)
        note: Note | None = scalar_result.one_or_none()
        if note is None:
            return None

        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if status is not None:
            note.status = status

        return note

class UserRepository:
    @staticmethod
    def get_user(session: Session, user_id: int) -> User | None:
        statement: Select[User] = (
            select(User)
            .where(User.id == user_id)
        )
        scalar_result: ScalarResult[User] = session.scalars(statement)
        return scalar_result.one_or_none()

    @staticmethod
    def create_user(session: Session, username: str, email: str) -> User:
        new_user: User = User(username=username, email=email)
        session.add(new_user)
        session.flush()
        return new_user
