import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_create_checkout_session(free_client: TestClient):
    with patch('stripe.checkout.Session.create') as mock_create:
        # Create a proper mock object with all required attributes
        mock_session = type('obj', (object,), {
            'id': 'test_session_id',
            'url': 'https://test.stripe.com/checkout',
            'client_reference_id': '1',
            'payment_status': 'unpaid'
        })
        mock_create.return_value = mock_session
        
        response = free_client.post("/api/v2/subscription/create-checkout-session")
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] == "test_session_id"
        assert "url" in data

def test_cancel_subscription(authorized_client: TestClient, test_user):
    with patch('app.services.stripe_service.stripe.Subscription.retrieve') as mock_retrieve:
        with patch('app.services.stripe_service.stripe.Subscription.modify') as mock_modify:
            mock_retrieve.return_value = type('obj', (object,), {
                'id': 'test_sub_id',
                'status': 'active'
            })
            
            response = authorized_client.post("/api/v2/subscription/cancel")
            assert response.status_code == 200
            assert response.json()["message"] == "Subscription cancelled successfully" 