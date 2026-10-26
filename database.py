from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base , sessionmaker
from config import settings

DB_URL = settings.database_url

engine = create_engine(DB_URL , pool_pre_ping=True)

SessionLocal = sessionmaker(bind = engine , autoflush=False , autocommit = False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()