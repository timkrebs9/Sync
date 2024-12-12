import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_create_checkout_session(authorized_client: TestClient):
    with patch('app.services.stripe_service.stripe.checkout.Session.create') as mock_create:
        mock_create.return_value.id = "test_session_id"
        response = authorized_client.post("/api/v2/subscription/create-checkout-session")
        assert response.status_code == 200
        assert "session_id" in response.json()

def test_cancel_subscription(authorized_client: TestClient, premium_user):
    with patch('app.services.stripe_service.stripe.Subscription.modify') as mock_modify:
        response = authorized_client.post("/api/v2/subscription/cancel")
        assert response.status_code == 200
        assert response.json()["message"] == "Subscription cancelled successfully" 