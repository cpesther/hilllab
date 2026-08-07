# Christopher Esther, Hill Lab, 7/16/2026
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from contextlib import contextmanager

from .config import DATABASE_PATH

engine = create_engine(
    f'sqlite:///{DATABASE_PATH}'
)

class Base(DeclarativeBase):
    pass

# Database session management
Session = sessionmaker(bind=engine)
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

