from typing import Iterator
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings


connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(settings.DATABASE_URL, echo=True, connect_args=connect_args)

def init_db() -> None:
    """ For develop mode, create all tables at once"""
    if settings.ENVIRONMENT == "DEV":
        SQLModel.metadata.create_all(engine)

def get_session() -> Iterator[Session]:
    """ Generator that yields database session """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e