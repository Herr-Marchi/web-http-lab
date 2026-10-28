from datetime import datetime

from pydantic import BaseModel

from data.models import Note, User

# чистые объекты ориентированные на переноску данных, ну и заодно документируемость за счет Pydantic
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    created_at: datetime
    user_id: int

    @classmethod
    def from_orm(cls, orm_note: Note) -> NoteResponse:
        return cls(
            id=orm_note.id,
            title=orm_note.title,
            content=orm_note.content,
            status=orm_note.status,
            created_at=orm_note.created_at,
            user_id=orm_note.user_id,
        )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    @classmethod
    def from_orm(cls, orm_user: User) -> UserResponse:
        return cls(
            id=orm_user.id,
            username=orm_user.username,
            email=orm_user.email,
        )
