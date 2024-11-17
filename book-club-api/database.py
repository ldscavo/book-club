from sqlmodel import SQLModel, create_engine
import settings

db_engine = create_engine(settings.DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(db_engine)
