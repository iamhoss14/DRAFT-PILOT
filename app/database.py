from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. HARDCODED CONNECTION (Bypassing .env completely)
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/draftpilot"

# 2. Connect Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()