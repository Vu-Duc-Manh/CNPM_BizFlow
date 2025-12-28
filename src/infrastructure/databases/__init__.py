from .base import Base
from .session import engine, SessionLocal


def init_db():
    Base.metadata.create_all(bind=engine)
