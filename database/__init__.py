from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from config import DatabaseConfig

Base = declarative_base()

engine = create_engine(
    DatabaseConfig.URL
)

session = sessionmaker(
    bind=engine
)

def init_db():
    Base.metadata.create_all(engine)

@contextmanager
def session_scope() -> Session:
    yield_session = session()
    try:
        yield yield_session

    finally:
        yield_session.close()
