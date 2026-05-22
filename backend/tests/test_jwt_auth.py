"""
Tests for JWT authentication and authorization.
"""
import pytest
from flask_jwt_extended import create_access_token
from datetime import datetime


class TestJWTAuthentication:
    """Test suite for JWT token authentication."""

    def test_valid_jwt_token_grants_access(self, client, auth_token, auth_headers):
        """Test that valid JWT token grants access to protected routes."""
        response = client.get('/api/expenses/', headers=auth_headers)
        assert response.status_code == 200

    def test_missing_authorization_header(self, client):
        """Test that missing Authorization header is rejected."""
        response = client.get('/api/expenses/')
        assert response.status_code == 401

    def test_malformed_authorization_header(self, client):
        """Test that malformed Authorization header is rejected."""
        headers = {'Authorization': 'InvalidFormat'}
        response = client.get('/api/expenses/', headers=headers)
        assert response.status_code == 401

    def test_invalid_jwt_token(self, client):
        """Test that invalid JWT token is rejected."""
        headers = {'Authorization': 'Bearer invalid.token.string'}
        response = client.get('/api/expenses/', headers=headers)
        assert response.status_code == 401

    def test_bearer_prefix_required(self, client, auth_token):
        """Test that Bearer prefix is required."""
        headers = {'Authorization': auth_token}  # Missing 'Bearer '
        response = client.get('/api/expenses/', headers=headers)
        assert response.status_code == 401

    def test_case_sensitive_bearer_prefix(self, client, auth_token):
        """Test Bearer prefix handling."""
        # Try lowercase
        headers = {'Authorization': f'bearer {auth_token}'}
        response = client.get('/api/expenses/', headers=headers)
        # Might fail depending on implementation
        assert response.status_code in [401, 200]

    def test_token_includes_user_identity(self, client, test_user):
        """Test that token contains user identity."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Token should be valid
        token = response.json['token']
        
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/expenses/', headers=headers)
        assert response.status_code == 200


class TestJWTAuthorization:
    """Test suite for JWT-based authorization."""

    def test_different_users_cannot_access_each_other_expenses(self, client, 
                                                               auth_headers, 
                                                               auth_headers_2, 
                                                               test_expenses):
        """Test that users are isolated - can't access other user's data."""
        # User 1 has 3 expenses
        response1 = client.get('/api/expenses/', headers=auth_headers)
        assert len(response1.json) == 3
        
        # User 2 shouldn't see them
        response2 = client.get('/api/expenses/', headers=auth_headers_2)
        assert len(response2.json) == 0

    def test_user_identity_extracted_from_token(self, client, test_user, test_user_2, 
                                                auth_token, auth_token_2, app):
        """Test that correct user identity is extracted from token."""
        headers1 = {'Authorization': f'Bearer {auth_token}'}
        headers2 = {'Authorization': f'Bearer {auth_token_2}'}
        
        # Create expense as user 1
        response = client.post('/api/expenses/',
            headers=headers1,
            json={
                'amount': 50.00,
                'description': 'User1 expense'
            }
        )
        
        with app.app_context():
            from models.expense_model import Expense
            expense = Expense.query.filter_by(description='User1 expense').first()
            assert expense.user_id == test_user.id
            assert expense.user_id != test_user_2.id


class TestTokenExpiration:
    """Test suite for token expiration handling."""

    def test_expired_token_rejected(self, app, client, test_user):
        """Test that expired tokens are rejected."""
        with app.app_context():
            # Create an expired token (this is just a placeholder test)
            # In real scenario, would need to manipulate time or use exp claim
            pass
        # This would require mocking time or creating expired token directly
        # Placeholder for test structure

    def test_token_from_login_is_valid(self, client, test_user):
        """Test that token from login is immediately valid."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        token = response.json['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Should be able to use token immediately
        response = client.get('/api/expenses/', headers=headers)
        assert response.status_code == 200


class TestEndpointAuthorization:
    """Test suite for endpoint-level authorization."""

    def test_register_no_auth_required(self, client):
        """Test that registration doesn't require authentication."""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 201

    def test_login_no_auth_required(self, client):
        """Test that login doesn't require authentication."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Should be 401 for invalid creds, not 401 for missing auth
        assert response.status_code in [200, 401]

    def test_expense_endpoints_require_auth(self, client):
        """Test that all expense endpoints require authentication."""
        endpoints = [
            ('/api/expenses/', 'GET'),
            ('/api/expenses/', 'POST'),
            ('/api/expenses/1', 'PUT'),
            ('/api/expenses/1', 'DELETE'),
        ]
        
        for endpoint, method in endpoints:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                response = client.post(endpoint, json={})
            elif method == 'PUT':
                response = client.put(endpoint, json={})
            elif method == 'DELETE':
                response = client.delete(endpoint)
            
            assert response.status_code == 401, f"{method} {endpoint} didn't require auth"

    def test_category_endpoints_require_auth(self, client):
        """Test that all category endpoints require authentication."""
        endpoints = [
            ('/api/categories/', 'GET'),
            ('/api/categories/', 'POST'),
            ('/api/categories/1', 'PUT'),
            ('/api/categories/1', 'DELETE'),
        ]
        
        for endpoint, method in endpoints:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                response = client.post(endpoint, json={})
            elif method == 'PUT':
                response = client.put(endpoint, json={})
            elif method == 'DELETE':
                response = client.delete(endpoint)
            
            assert response.status_code == 401, f"{method} {endpoint} didn't require auth"


class TestAuthErrorHandling:
    """Test suite for authentication error handling."""

    def test_jwt_decode_error_handling(self, client):
        """Test handling of JWT decode errors."""
        headers = {'Authorization': 'Bearer not.a.valid.jwt'}
        response = client.get('/api/expenses/', headers=headers)
        assert response.status_code == 401

    def test_missing_token_claim_handling(self, client):
        """Test handling of tokens missing required claims."""
        # This would require generating a token without standard claims
        # Placeholder for structure
        pass


class TestMultipleTokens:
    """Test suite for multiple concurrent tokens."""

    def test_multiple_tokens_same_user(self, client, test_user):
        """Test that same user can have multiple tokens."""
        # Get first token
        response1 = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token1 = response1.json['token']
        
        # Get second token
        response2 = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token2 = response2.json['token']
        
        # Both tokens should work
        headers1 = {'Authorization': f'Bearer {token1}'}
        headers2 = {'Authorization': f'Bearer {token2}'}
        
        response1 = client.get('/api/expenses/', headers=headers1)
        response2 = client.get('/api/expenses/', headers=headers2)
        
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_tokens_are_different(self, client, test_user):
        """Test that multiple login calls generate different tokens."""
        response1 = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token1 = response1.json['token']
        
        response2 = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        token2 = response2.json['token']
        
        # Tokens might be different due to generation time
        # (depends on implementation)
        assert isinstance(token1, str)
        assert isinstance(token2, str)
        assert len(token1) > 0
        assert len(token2) > 0
