from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def create_table():
    from src.db.model import ChatHistory

    print("Table creating")
    Base.metadata.create_all(bind=engine)
    print("Table Created")
