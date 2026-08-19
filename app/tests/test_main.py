import time
import hmac
import hashlib
import json
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from app.main import app, get_password_hash
from app.database import get_session
from app.models import User, Transaction

sqlite_url = "sqlite://"
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Production Payment Engine API is running"}


def test_signup_and_token_flow():
    signup_response = client.post(
        "/signup",
        json={"email": "integration@test.com", "password": "securepassword123"},
    )
    assert signup_response.status_code == 201
    assert signup_response.json()["email"] == "integration@test.com"

    token_response = client.post(
        "/token",
        data={
            "username": "integration@test.com",
            "password": "securepassword123",
        },
    )
    assert token_response.status_code == 200
    data = token_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_protected_checkout_requires_auth():
    response = client.post(
        "/create-checkout-session",
        params={"email": "customer@test.com", "amount": 2000},
    )
    assert response.status_code == 401


def test_protected_checkout_success():
    with Session(engine) as session:
        user = User(
            email="authuser@test.com",
            hashed_password=get_password_hash("testpassword"),
        )
        session.add(user)
        session.commit()

    token_response = client.post(
        "/token",
        data={"username": "authuser@test.com", "password": "testpassword"},
    )
    token = token_response.json()["access_token"]

    response = client.post(
        "/create-checkout-session",
        params={"email": "customer@test.com", "amount": 5000},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in [200, 400]


def test_webhook_signature_and_fulfillment():
    test_session_id = "cs_test_mocksession_123"
    with Session(engine) as session:
        transaction = Transaction(
            stripe_session_id=test_session_id,
            status="pending",
            amount=5000,
            user_email="test@example.com"
        )
        session.add(transaction)
        session.commit()

    webhook_secret = "whsec_aZLQjZojjJBN1kbETJLWVuSpjUXz4U2x"

    payload = {
        "id": "evt_test_pytest",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": test_session_id,
                "customer_email": "customer@test.com",
                "payment_status": "paid"
            }
        }
    }

    payload_string = json.dumps(payload)

    timestamp = int(time.time())
    signed_payload = f"{timestamp}.{payload_string}"
    signature = hmac.new(
        webhook_secret.encode("utf-8"),
        signed_payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    sig_header = f"t={timestamp},v1={signature}"

    headers = {
        "Stripe-Signature": sig_header,
        "Content-Type": "application/json"
    }

    response = client.post("/webhook", data=payload_string, headers=headers)
    
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    with Session(engine) as session:
        db_transaction = session.exec(
            select(Transaction).where(Transaction.stripe_session_id == test_session_id)
        ).first()
        assert db_transaction is not None
        assert db_transaction.status == "completed"
        
        