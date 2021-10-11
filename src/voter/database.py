from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import setting

engine = create_engine(setting.database_url)


Session = sessionmaker(engine, autocommit=False, autoflush=False)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()
