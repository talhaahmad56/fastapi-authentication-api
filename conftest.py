import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base ,  get_db
from main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread" : False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(bind=engine , autoflush= False , autocommit = False)

@pytest.fixture
def clients():
    Base.metadata.create_all(bind = engine)

    def override_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind = engine)            