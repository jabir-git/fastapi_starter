from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine

# Database URL
DATABASE_URL = "sqlite:///./test.sqlite3"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)


# Define your models here
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    age: Optional[int] = None


# Create tables
def create_db_tables():
    SQLModel.metadata.create_all(engine)


# Get session dependency
def get_session():
    with Session(engine) as session:
        yield session
