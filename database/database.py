from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///cafe.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)


def get_db():
    # Get a database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
