import pytest
from fastapi.testclient import TestClient
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.user_model import User, SubscriptionTier, UserRole
from app.core.security import get_password_hash, create_access_token

# Set testing environment variables
os.environ["TESTING"] = "true"
os.environ["STRIPE_SECRET_KEY"] = os.getenv("STRIPE_SECRET_KEY", "sk_test_dummy")
os.environ["STRIPE_WEBHOOK_SECRET"] = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_dummy")
os.environ["STRIPE_PRICE_ID"] = os.getenv("STRIPE_PRICE_ID", "price_dummy")

# Check if we're running in CI environment
IS_CI = os.getenv("CI", "false").lower() == "true"

if IS_CI:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/snyc_test"
else:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DATABASE_URL')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}?sslmode=require"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpass123"),
        role=UserRole.USER,
        subscription=SubscriptionTier.PREMIUM,
        stripe_subscription_id="test_sub_id"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_user_token(test_user):
    return create_access_token(data={"sub": test_user.username})

@pytest.fixture
def authorized_client(client, test_user_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {test_user_token}"
    }
    return client

@pytest.fixture
def premium_user(db_session):
    user = User(
        email="premium@example.com",
        username="premiumuser",
        hashed_password=get_password_hash("password"),
        role=UserRole.USER,
        subscription=SubscriptionTier.PREMIUM
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def admin_user(db_session):
    user = User(
        email="admin@example.com",
        username="adminuser",
        hashed_password=get_password_hash("password"),
        role=UserRole.ADMIN,
        subscription=SubscriptionTier.PREMIUM
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def free_user(db_session):
    user = User(
        email="free@example.com",
        username="freeuser",
        hashed_password=get_password_hash("testpass123"),
        role=UserRole.USER,
        subscription=SubscriptionTier.FREE
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def free_client(client, free_user):
    token = create_access_token(data={"sub": free_user.username})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
