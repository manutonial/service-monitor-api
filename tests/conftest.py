import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models.check_result  # noqa: F401
import app.models.service  # noqa: F401
from app.api.dependencies import get_db
from app.core.database import Base
from app.main import app as fastapi_app

# StaticPool forces all connections to share the same in-memory database.
# Without it, each new connection to sqlite:///:memory: gets a fresh empty DB.
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(autouse=True)
def reset_database():
    """
    Create all tables before each test, drop them afterwards.
    autouse=True means this fixture runs automatically for every test.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Isolated database session for direct data manipulation inside tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """
    FastAPI TestClient backed by the in-memory test database.
    Overrides the get_db dependency so every request uses the test session.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fastapi_app) as test_client:
        yield test_client

    fastapi_app.dependency_overrides.clear()
