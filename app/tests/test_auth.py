from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app
import pytest

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_user():
    # Register first user
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    # Try to register same user again
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400

def test_login_user():
    # Register user first
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    # Try to login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    # Register user first
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401 