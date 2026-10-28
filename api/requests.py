from typing import Self

from pydantic import BaseModel, Field, model_validator


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)
    status: str = Field(min_length=1, max_length=20)
    user_id: int = Field(gt=0)


class NotePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=80)
    content: str | None = Field(default=None, min_length=1, max_length=500)
    status: str | None = Field(default=None, min_length=1, max_length=20)

    @model_validator(mode="after")
    def require_change(self) -> Self:
        """Я хочу чтобы был разрешен только патч который содержит хоть одно из полей в body с не null значением,
        поэтому добавил дополнительную валидацию на кейс где все 3 поля None после создания объекта.
        Должна 422 вернуться если эта проверка провалится, Pydantic перехватит мой ValueError,
        и превратит в ошибку валидации, при которой FastAPI 422 отдаст
        """
        if self.title is None and self.content is None and self.status is None:
            raise ValueError("At least one of title, content or status is required")

        return self


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1, max_length=100)
