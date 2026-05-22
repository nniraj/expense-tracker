"""
Pytest configuration and fixtures for expense tracker backend tests.
"""
import pytest
import os
from dotenv import load_dotenv

# Load environment variables from .env file BEFORE importing app
# This must be done before any imports that use config
load_dotenv()

# Set default environment variables for testing if not already set
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgresql://postgres:Vedant%40065@localhost/expense_tracker'

if not os.getenv('JWT_SECRET_KEY'):
    os.environ['JWT_SECRET_KEY'] = 'test-secret-key-for-development'

if not os.getenv('TEST_DATABASE_URL'):
    os.environ['TEST_DATABASE_URL'] = 'postgresql://postgres:Vedant%40065@localhost/expense_tracker_test'

# Now import app and models AFTER environment variables are set
from app import create_app
from extensions import db
from models.user_models import User
from models.category_model import Category
from models.expense_model import Expense


@pytest.fixture(scope='function')
def app():
    """
    Create and configure a test Flask application.
    """
    app = create_app()
    
    # Use test database configuration
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 
                                                        'postgresql://postgres:Vedant%40065@localhost/expense_tracker_test')
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    # Create application context
    with app.app_context():
        # Create all tables
        db.create_all()
        yield app
        # Clean up after test
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a CLI runner for the Flask application.
    """
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """
    Create a test user in the database.
    """
    user = User(
        username='testuser',
        email='test@example.com'
    )
    user.set_password('password123')
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def test_user_2(app):
    """
    Create a second test user for testing user isolation.
    """
    user = User(
        username='testuser2',
        email='test2@example.com'
    )
    user.set_password('password456')
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def test_categories(app):
    """
    Create test categories in the database.
    """
    categories = [
        Category(name='Food'),
        Category(name='Transport'),
        Category(name='Entertainment'),
        Category(name='Utilities'),
    ]
    
    with app.app_context():
        for category in categories:
            db.session.add(category)
        db.session.commit()
        return categories


@pytest.fixture
def test_expenses(app, test_user, test_categories):
    """
    Create test expenses for a user.
    """
    expenses = [
        Expense(
            amount=50.00,
            description='Lunch',
            category_id=test_categories[0].id,
            user_id=test_user.id
        ),
        Expense(
            amount=25.50,
            description='Taxi ride',
            category_id=test_categories[1].id,
            user_id=test_user.id
        ),
        Expense(
            amount=100.00,
            description='Movie tickets',
            category_id=test_categories[2].id,
            user_id=test_user.id
        ),
    ]
    
    with app.app_context():
        for expense in expenses:
            db.session.add(expense)
        db.session.commit()
        return expenses


@pytest.fixture
def auth_token(client, test_user):
    """
    Get JWT token for test user.
    """
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    return response.json['token']


@pytest.fixture
def auth_headers(auth_token):
    """
    Create authorization headers with JWT token.
    """
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def auth_token_2(client, test_user_2):
    """
    Get JWT token for second test user.
    """
    response = client.post('/api/auth/login', json={
        'email': 'test2@example.com',
        'password': 'password456'
    })
    return response.json['token']


@pytest.fixture
def auth_headers_2(auth_token_2):
    """
    Create authorization headers with second user's JWT token.
    """
    return {
        'Authorization': f'Bearer {auth_token_2}',
        'Content-Type': 'application/json'
    }
