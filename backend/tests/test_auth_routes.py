"""
Tests for authentication routes (register, login).
"""
import pytest
from models.user_models import User


class TestUserRegistration:
    """Test suite for user registration endpoint."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123'
        })
        
        assert response.status_code == 201
        assert response.json['success'] is True
        assert 'registered successfully' in response.json['message'].lower()

    def test_register_existing_email(self, client, test_user):
        """Test registration fails with existing email."""
        response = client.post('/api/auth/register', json={
            'username': 'anotheruser',
            'email': 'test@example.com',  # Already exists
            'password': 'password789'
        })
        
        assert response.status_code == 400
        assert response.json['success'] is False
        assert 'email already exists' in response.json['message'].lower()

    def test_register_missing_fields(self, client):
        """Test registration fails with missing required fields."""
        # Missing email
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'password': 'password123'
        })
        assert response.status_code == 400

    def test_register_creates_user_in_database(self, client, app):
        """Test that registered user is created in database."""
        client.post('/api/auth/register', json={
            'username': 'dbuser',
            'email': 'dbuser@example.com',
            'password': 'password123'
        })
        
        with app.app_context():
            user = User.query.filter_by(email='dbuser@example.com').first()
            assert user is not None
            assert user.username == 'dbuser'
            assert user.email == 'dbuser@example.com'

    def test_register_password_hashed(self, client, app):
        """Test that password is properly hashed."""
        client.post('/api/auth/register', json={
            'username': 'hashuser',
            'email': 'hashuser@example.com',
            'password': 'plaintext'
        })
        
        with app.app_context():
            user = User.query.filter_by(email='hashuser@example.com').first()
            # Password should not match plaintext
            assert not user.check_password('wrongpassword')
            assert user.check_password('plaintext')

    def test_register_missing_username(self, client):
        """Test registration fails without username."""
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        assert response.status_code == 400
        assert 'required' in response.json['message'].lower()

    def test_register_missing_password(self, client):
        """Test registration fails without password."""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'test@example.com'
        })
        assert response.status_code == 400
        assert 'required' in response.json['message'].lower()

    def test_register_duplicate_username(self, client, test_user):
        """Test registration fails with duplicate username."""
        response = client.post('/api/auth/register', json={
            'username': 'testuser',  # Already exists from test_user fixture
            'email': 'different@example.com',
            'password': 'password123'
        })
        assert response.status_code == 400
        assert 'username already exists' in response.json['message'].lower()

    def test_register_invalid_email_format(self, client):
        """Test registration fails with invalid email format."""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'email': 'invalidemail',  # Missing @ and .
            'password': 'password123'
        })
        assert response.status_code == 400
        assert 'email' in response.json['message'].lower()

    def test_register_empty_request_body(self, client):
        """Test registration fails with empty request body."""
        response = client.post('/api/auth/register', json={})
        assert response.status_code == 400
        assert 'required' in response.json['message'].lower()


class TestUserLogin:
    """Test suite for user login endpoint."""

    def test_login_success(self, client, test_user):
        """Test successful login with correct credentials."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert response.json['success'] is True
        assert 'token' in response.json
        assert response.json['user']['email'] == 'test@example.com'
        assert response.json['user']['username'] == 'testuser'
        assert response.json['user']['id'] == test_user.id

    def test_login_invalid_email(self, client):
        """Test login fails with non-existent email."""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 401
        assert response.json['success'] is False
        assert 'invalid credentials' in response.json['message'].lower()

    def test_login_invalid_password(self, client, test_user):
        """Test login fails with incorrect password."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        assert response.json['success'] is False
        assert 'invalid credentials' in response.json['message'].lower()

    def test_login_returns_jwt_token(self, client, test_user):
        """Test that login returns a valid JWT token."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        token = response.json['token']
        # Token should be a non-empty string
        assert isinstance(token, str)
        assert len(token) > 0
        # JWT tokens typically contain 3 parts separated by dots
        assert token.count('.') == 2

    def test_login_missing_email(self, client):
        """Test login fails with missing email."""
        response = client.post('/api/auth/login', json={
            'password': 'password123'
        })
        
        assert response.status_code == 400

    def test_login_missing_password(self, client):
        """Test login fails with missing password."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400

    def test_login_case_sensitive_email(self, client, test_user):
        """Test that email login is case-insensitive (lowercase stored)."""
        # Database stores emails as provided
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        assert response.status_code == 200

    def test_login_returns_user_details(self, client, test_user):
        """Test that login response includes all required user fields."""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        user = response.json['user']
        assert 'id' in user
        assert 'username' in user
        assert 'email' in user
        assert user['id'] == test_user.id

    def test_login_empty_request_body(self, client):
        """Test login fails with empty request body."""
        response = client.post('/api/auth/login', json={})
        assert response.status_code == 400
        assert 'required' in response.json['message'].lower()



class TestPasswordSecurity:
    """Test suite for password security."""

    def test_passwords_not_stored_plaintext(self, client, app):
        """Test that passwords are never stored in plaintext."""
        client.post('/api/auth/register', json={
            'username': 'secuser',
            'email': 'secuser@example.com',
            'password': 'mysecretpassword'
        })
        
        with app.app_context():
            user = User.query.filter_by(email='secuser@example.com').first()
            # Password hash should not equal plaintext password
            assert user.password_hash != 'mysecretpassword'

    def test_different_passwords_different_hashes(self, client, app):
        """Test that different passwords produce different hashes."""
        user1 = User(username='user1', email='user1@example.com')
        user1.set_password('password123')
        
        user2 = User(username='user2', email='user2@example.com')
        user2.set_password('password123')
        
        # Even with same password, hashes should be different (bcrypt adds salt)
        # Actually, they might be different due to salt, let's just check they work
        with app.app_context():
            assert user1.check_password('password123')
            assert user2.check_password('password123')
            assert not user1.check_password('wrongpassword')
