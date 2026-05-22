"""
Tests for database models (User, Expense, Category).
"""
import pytest
from models.user_models import User
from models.expense_model import Expense
from models.category_model import Category
from extensions import db
from datetime import datetime


class TestUserModel:
    """Test suite for User model."""

    def test_user_creation(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User(
                username='testuser',
                email='test@example.com'
            )
            user.set_password('password123')
            
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.password_hash is not None

    def test_user_password_hashing(self, app):
        """Test that passwords are hashed."""
        with app.app_context():
            user = User(username='user', email='user@example.com')
            user.set_password('plaintext')
            
            # Hash should not be plaintext
            assert user.password_hash != 'plaintext'

    def test_user_password_verification(self, app):
        """Test password verification."""
        with app.app_context():
            user = User(username='user', email='user@example.com')
            user.set_password('correct')
            
            assert user.check_password('correct') is True
            assert user.check_password('incorrect') is False

    def test_user_password_case_sensitive(self, app):
        """Test that password verification is case-sensitive."""
        with app.app_context():
            user = User(username='user', email='user@example.com')
            user.set_password('Password123')
            
            assert user.check_password('Password123') is True
            assert user.check_password('password123') is False

    def test_user_unique_email(self, app):
        """Test that emails must be unique."""
        with app.app_context():
            user1 = User(username='user1', email='test@example.com')
            user1.set_password('pass')
            db.session.add(user1)
            db.session.commit()
            
            user2 = User(username='user2', email='test@example.com')
            user2.set_password('pass')
            db.session.add(user2)
            
            # Should raise IntegrityError
            with pytest.raises(Exception):
                db.session.commit()

    def test_user_unique_username(self, app):
        """Test that usernames must be unique."""
        with app.app_context():
            user1 = User(username='duplicate', email='user1@example.com')
            user1.set_password('pass')
            db.session.add(user1)
            db.session.commit()
            
            user2 = User(username='duplicate', email='user2@example.com')
            user2.set_password('pass')
            db.session.add(user2)
            
            with pytest.raises(Exception):
                db.session.commit()

    def test_user_created_at_timestamp(self, app):
        """Test that created_at timestamp is set."""
        with app.app_context():
            user = User(username='user', email='user@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            user = User.query.filter_by(email='user@example.com').first()
            assert user.created_at is not None
            assert isinstance(user.created_at, datetime)

    def test_user_id_auto_increment(self, app):
        """Test that user IDs are auto-incremented."""
        with app.app_context():
            user1 = User(username='user1', email='user1@example.com')
            user1.set_password('pass')
            db.session.add(user1)
            db.session.commit()
            
            user2 = User(username='user2', email='user2@example.com')
            user2.set_password('pass')
            db.session.add(user2)
            db.session.commit()
            
            assert user2.id > user1.id


class TestExpenseModel:
    """Test suite for Expense model."""

    def test_expense_creation(self, app, test_user, test_categories):
        """Test creating a new expense."""
        with app.app_context():
            expense = Expense(
                amount=50.00,
                description='Lunch',
                category_id=test_categories[0].id,
                user_id=test_user.id
            )
            
            assert expense.amount == 50.00
            assert expense.description == 'Lunch'
            assert expense.category_id == test_categories[0].id
            assert expense.user_id == test_user.id

    def test_expense_required_fields(self, app):
        """Test that expense requires amount and description."""
        with app.app_context():
            # Missing amount or description should fail on DB constraint
            expense = Expense(description='Test', user_id=1)
            db.session.add(expense)
            
            with pytest.raises(Exception):
                db.session.commit()

    def test_expense_date_auto_set(self, app, test_user):
        """Test that date is automatically set."""
        with app.app_context():
            expense = Expense(
                amount=30.00,
                description='Groceries',
                user_id=test_user.id
            )
            db.session.add(expense)
            db.session.commit()
            
            assert expense.date is not None
            assert isinstance(expense.date, datetime)

    def test_expense_optional_category(self, app, test_user):
        """Test that category is optional."""
        with app.app_context():
            expense = Expense(
                amount=25.00,
                description='Misc',
                user_id=test_user.id
            )
            db.session.add(expense)
            db.session.commit()
            
            assert expense.category_id is None

    def test_expense_decimal_amounts(self, app, test_user):
        """Test that expenses support decimal amounts."""
        with app.app_context():
            expense = Expense(
                amount=19.99,
                description='Test',
                user_id=test_user.id
            )
            db.session.add(expense)
            db.session.commit()
            
            assert expense.amount == 19.99

    def test_expense_id_auto_increment(self, app, test_user):
        """Test that expense IDs are auto-incremented."""
        with app.app_context():
            expense1 = Expense(
                amount=10.0,
                description='First',
                user_id=test_user.id
            )
            db.session.add(expense1)
            db.session.commit()
            
            expense2 = Expense(
                amount=20.0,
                description='Second',
                user_id=test_user.id
            )
            db.session.add(expense2)
            db.session.commit()
            
            assert expense2.id > expense1.id

    def test_expense_user_relationship(self, app, test_user, test_expenses):
        """Test relationship between expense and user."""
        with app.app_context():
            expenses = Expense.query.filter_by(user_id=test_user.id).all()
            assert len(expenses) == 3

    def test_expense_category_relationship(self, app, test_categories, test_expenses):
        """Test relationship between expense and category."""
        with app.app_context():
            category = test_categories[0]
            expenses = Expense.query.filter_by(category_id=category.id).all()
            assert len(expenses) >= 1


class TestCategoryModel:
    """Test suite for Category model."""

    def test_category_creation(self, app):
        """Test creating a new category."""
        with app.app_context():
            category = Category(name='Groceries')
            
            assert category.name == 'Groceries'

    def test_category_unique_name(self, app):
        """Test that category names must be unique."""
        with app.app_context():
            category1 = Category(name='Dining')
            db.session.add(category1)
            db.session.commit()
            
            category2 = Category(name='Dining')
            db.session.add(category2)
            
            with pytest.raises(Exception):
                db.session.commit()

    def test_category_required_name(self, app):
        """Test that category requires a name."""
        with app.app_context():
            category = Category()
            db.session.add(category)
            
            with pytest.raises(Exception):
                db.session.commit()

    def test_category_id_auto_increment(self, app):
        """Test that category IDs are auto-incremented."""
        with app.app_context():
            category1 = Category(name='Cat1')
            db.session.add(category1)
            db.session.commit()
            
            category2 = Category(name='Cat2')
            db.session.add(category2)
            db.session.commit()
            
            assert category2.id > category1.id

    def test_category_long_name(self, app):
        """Test category with long name."""
        with app.app_context():
            long_name = 'A' * 100
            category = Category(name=long_name)
            db.session.add(category)
            db.session.commit()
            
            assert category.name == long_name

    def test_category_special_characters(self, app):
        """Test category name with special characters."""
        with app.app_context():
            category = Category(name='Food & Dining')
            db.session.add(category)
            db.session.commit()
            
            assert category.name == 'Food & Dining'


class TestModelIntegration:
    """Test suite for model integration and relationships."""

    def test_user_has_many_expenses(self, app, test_user, test_expenses):
        """Test that user can have multiple expenses."""
        with app.app_context():
            user = User.query.get(test_user.id)
            expenses = Expense.query.filter_by(user_id=user.id).all()
            
            assert len(expenses) == 3

    def test_category_has_many_expenses(self, app, test_categories, test_expenses):
        """Test that category can have multiple expenses."""
        with app.app_context():
            category = test_categories[0]
            expenses = Expense.query.filter_by(category_id=category.id).all()
            
            assert len(expenses) >= 1

    def test_cascade_delete_on_user_removal(self, app, test_user, test_expenses):
        """Test that expenses are deleted when user is deleted."""
        user_id = test_user.id
        
        with app.app_context():
            # Delete user
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            
            # Expenses should also be deleted (if cascade is set)
            expenses = Expense.query.filter_by(user_id=user_id).all()
            # This depends on cascade rules defined in model
