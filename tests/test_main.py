import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from database import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
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
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_create_customer():
    response = client.post(
        "/customers/",
        json={"name": "John Doe", "phone": "1234567890", "email": "john@example.com", "address": "123 Main St"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data

def test_create_loan():
    # First create a customer
    client.post(
        "/customers/",
        json={"name": "John Doe", "phone": "1234567890"},
    )

    response = client.post(
        "/loans/",
        json={"customer_id": 1, "principal": 1000.0, "interest_rate": 10.0, "duration_days": 10},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["principal"] == 1000.0
    assert data["status"] == "active"

def test_loan_status_calculation():
    # Setup: Customer + Loan
    client.post("/customers/", json={"name": "Jane Doe", "phone": "0987654321"})
    client.post("/loans/", json={"customer_id": 1, "principal": 1000.0, "interest_rate": 10.0, "duration_days": 10})

    # Total repayment should be 1100 (1000 + 10%)
    # Daily installment should be 110 (1100 / 10)

    response = client.get("/loans/1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["total_repayment"] == 1100.0
    assert data["daily_installment"] == 110.0
    assert data["remaining_balance"] == 1100.0

    # Add a repayment
    client.post("/repayments/", json={"loan_id": 1, "amount": 220.0})

    response = client.get("/loans/1/status")
    data = response.json()
    assert data["amount_paid"] == 220.0
    assert data["remaining_balance"] == 880.0
    assert data["status"] == "active"

def test_loan_fully_paid():
    client.post("/customers/", json={"name": "Jane Doe", "phone": "0987654321"})
    client.post("/loans/", json={"customer_id": 1, "principal": 100.0, "interest_rate": 0.0, "duration_days": 1})

    client.post("/repayments/", json={"loan_id": 1, "amount": 100.0})

    response = client.get("/loans/1/status")
    data = response.json()
    assert data["remaining_balance"] == 0.0
    assert data["status"] == "paid"
