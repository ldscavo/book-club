from sqlmodel import SQLModel, create_engine, Session
import settings

db_engine = create_engine(settings.DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(db_engine)


def get_session():
    with Session(db_engine) as session:
        yield session
