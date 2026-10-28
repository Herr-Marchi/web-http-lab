from fastapi import FastAPI

from api import setup_routes
from data import NoteRepository, UserRepository


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="Notes API", version="0.1.0")
    setup_routes(app, NoteRepository(), UserRepository())
    return app


app: FastAPI = create_app()
