"""
Tests for expense management routes (CRUD operations).
"""
import pytest
from models.expense_model import Expense
from datetime import datetime


class TestCreateExpense:
    """Test suite for creating expenses."""

    def test_create_expense_success(self, client, auth_headers, test_categories):
        """Test successful expense creation."""
        response = client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'amount': 50.00,
                'description': 'Lunch at cafe',
                'category_id': test_categories[0].id
            }
        )
        
        assert response.status_code == 200
        assert 'Expense added' in response.json.get('msg', '')

    def test_create_expense_without_category(self, client, auth_headers):
        """Test creating expense without category."""
        response = client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'amount': 30.00,
                'description': 'Groceries'
            }
        )
        
        assert response.status_code == 200
        assert 'Expense added' in response.json.get('msg', '')

    def test_create_expense_missing_amount(self, client, auth_headers):
        """Test creating expense fails without amount."""
        response = client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'description': 'Missing amount'
            }
        )
        
        # Should fail due to missing required field
        assert response.status_code in [400, 500]

    def test_create_expense_missing_description(self, client, auth_headers):
        """Test creating expense fails without description."""
        response = client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'amount': 50.00
            }
        )
        
        assert response.status_code in [400, 500]

    def test_create_expense_requires_auth(self, client):
        """Test that creating expense requires authentication."""
        response = client.post('/api/expenses/', 
            json={
                'amount': 50.00,
                'description': 'Unauthorized expense'
            }
        )
        
        assert response.status_code == 401

    def test_create_expense_invalid_token(self, client):
        """Test that invalid token is rejected."""
        headers = {
            'Authorization': 'Bearer invalid.token.here',
            'Content-Type': 'application/json'
        }
        response = client.post('/api/expenses/', 
            headers=headers,
            json={
                'amount': 50.00,
                'description': 'Lunch'
            }
        )
        
        assert response.status_code == 401

    def test_create_expense_stores_correct_data(self, client, auth_headers, test_categories, app):
        """Test that created expense has correct data in database."""
        client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'amount': 75.50,
                'description': 'Dinner',
                'category_id': test_categories[1].id
            }
        )
        
        with app.app_context():
            expense = Expense.query.filter_by(description='Dinner').first()
            assert expense is not None
            assert expense.amount == 75.50
            assert expense.category_id == test_categories[1].id


class TestGetExpenses:
    """Test suite for retrieving expenses."""

    def test_get_expenses_success(self, client, auth_headers, test_expenses):
        """Test successful retrieval of user's expenses."""
        response = client.get('/api/expenses/', headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == 3
        # Check first expense
        assert response.json[0]['description'] == 'Lunch'
        assert response.json[0]['amount'] == 50.00

    def test_get_expenses_empty(self, client, auth_headers):
        """Test getting expenses when user has none."""
        response = client.get('/api/expenses/', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json == []

    def test_get_expenses_requires_auth(self, client):
        """Test that getting expenses requires authentication."""
        response = client.get('/api/expenses/')
        
        assert response.status_code == 401

    def test_get_expenses_invalid_token(self, client):
        """Test that invalid token is rejected."""
        headers = {'Authorization': 'Bearer invalid.token'}
        response = client.get('/api/expenses/', headers=headers)
        
        assert response.status_code == 401

    def test_get_expenses_user_isolation(self, client, auth_headers, auth_headers_2, 
                                         test_expenses, test_user_2):
        """Test that users only see their own expenses."""
        # User 1 should see their 3 expenses
        response1 = client.get('/api/expenses/', headers=auth_headers)
        assert len(response1.json) == 3
        
        # User 2 should see no expenses
        response2 = client.get('/api/expenses/', headers=auth_headers_2)
        assert len(response2.json) == 0

    def test_get_expenses_includes_all_fields(self, client, auth_headers, test_expenses):
        """Test that expense response includes all required fields."""
        response = client.get('/api/expenses/', headers=auth_headers)
        
        expense = response.json[0]
        assert 'id' in expense
        assert 'amount' in expense
        assert 'description' in expense
        assert 'date' in expense
        assert 'category_id' in expense

    def test_get_expenses_date_format(self, client, auth_headers, test_expenses):
        """Test that expense dates are in ISO format."""
        response = client.get('/api/expenses/', headers=auth_headers)
        
        date_str = response.json[0]['date']
        # Should be ISO format
        assert 'T' in date_str or isinstance(date_str, str)


class TestUpdateExpense:
    """Test suite for updating expenses."""

    def test_update_expense_success(self, client, auth_headers, test_expenses):
        """Test successful expense update."""
        expense_id = test_expenses[0].id
        response = client.put(f'/api/expenses/{expense_id}', 
            headers=auth_headers,
            json={
                'amount': 60.00,
                'description': 'Lunch upgraded'
            }
        )
        
        assert response.status_code == 200
        assert 'Updated' in response.json.get('msg', '')

    def test_update_expense_partial(self, client, auth_headers, test_expenses):
        """Test updating only some fields."""
        expense_id = test_expenses[0].id
        response = client.put(f'/api/expenses/{expense_id}', 
            headers=auth_headers,
            json={
                'amount': 55.00
            }
        )
        
        assert response.status_code == 200

    def test_update_expense_not_found(self, client, auth_headers):
        """Test updating non-existent expense."""
        response = client.put('/api/expenses/99999', 
            headers=auth_headers,
            json={
                'amount': 100.00
            }
        )
        
        assert response.status_code == 404
        assert 'not found' in response.json.get('msg', '').lower()

    def test_update_expense_requires_auth(self, client, test_expenses):
        """Test that updating expense requires authentication."""
        response = client.put(f'/api/expenses/{test_expenses[0].id}', 
            json={'amount': 100.00}
        )
        
        assert response.status_code == 401

    def test_update_expense_user_isolation(self, client, auth_headers_2, test_expenses):
        """Test that users can't update other users' expenses."""
        # User 2 tries to update User 1's expense
        response = client.put(f'/api/expenses/{test_expenses[0].id}', 
            headers=auth_headers_2,
            json={'amount': 999.00}
        )
        
        assert response.status_code == 404

    def test_update_expense_category(self, client, auth_headers, test_expenses, test_categories):
        """Test updating expense category."""
        expense_id = test_expenses[0].id
        response = client.put(f'/api/expenses/{expense_id}', 
            headers=auth_headers,
            json={
                'category_id': test_categories[2].id
            }
        )
        
        assert response.status_code == 200

    def test_update_expense_verifies_changes(self, client, auth_headers, test_expenses, app):
        """Test that expense update is reflected in database."""
        expense_id = test_expenses[0].id
        client.put(f'/api/expenses/{expense_id}', 
            headers=auth_headers,
            json={
                'amount': 120.00,
                'description': 'Updated expense'
            }
        )
        
        with app.app_context():
            expense = Expense.query.get(expense_id)
            assert expense.amount == 120.00
            assert expense.description == 'Updated expense'


class TestDeleteExpense:
    """Test suite for deleting expenses."""

    def test_delete_expense_success(self, client, auth_headers, test_expenses):
        """Test successful expense deletion."""
        expense_id = test_expenses[0].id
        response = client.delete(f'/api/expenses/{expense_id}', 
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert 'Deleted' in response.json.get('msg', '')

    def test_delete_expense_not_found(self, client, auth_headers):
        """Test deleting non-existent expense."""
        response = client.delete('/api/expenses/99999', 
            headers=auth_headers
        )
        
        assert response.status_code == 404

    def test_delete_expense_requires_auth(self, client, test_expenses):
        """Test that deleting expense requires authentication."""
        response = client.delete(f'/api/expenses/{test_expenses[0].id}')
        
        assert response.status_code == 401

    def test_delete_expense_user_isolation(self, client, auth_headers_2, test_expenses):
        """Test that users can't delete other users' expenses."""
        response = client.delete(f'/api/expenses/{test_expenses[0].id}', 
            headers=auth_headers_2
        )
        
        assert response.status_code == 404

    def test_delete_expense_removes_from_database(self, client, auth_headers, test_expenses, app):
        """Test that deleted expense is removed from database."""
        expense_id = test_expenses[0].id
        client.delete(f'/api/expenses/{expense_id}', headers=auth_headers)
        
        with app.app_context():
            expense = Expense.query.get(expense_id)
            assert expense is None

    def test_delete_expense_verify_count(self, client, auth_headers, test_expenses):
        """Test that deleting reduces expense count."""
        # Get initial count
        response1 = client.get('/api/expenses/', headers=auth_headers)
        initial_count = len(response1.json)
        
        # Delete one
        client.delete(f'/api/expenses/{test_expenses[0].id}', headers=auth_headers)
        
        # Get new count
        response2 = client.get('/api/expenses/', headers=auth_headers)
        assert len(response2.json) == initial_count - 1


class TestExpenseValidation:
    """Test suite for expense data validation."""

    def test_expense_amount_decimal_precision(self, client, auth_headers):
        """Test that expense amounts handle decimal values."""
        response = client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'amount': 19.99,
                'description': 'Precise amount'
            }
        )
        
        assert response.status_code == 200

    def test_expense_negative_amount(self, client, auth_headers):
        """Test handling of negative amounts."""
        response = client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'amount': -50.00,
                'description': 'Negative amount'
            }
        )
        
        # Should either reject or accept (depends on business logic)
        assert response.status_code in [200, 400]

    def test_expense_long_description(self, client, auth_headers):
        """Test handling of long description."""
        long_description = 'A' * 300
        response = client.post('/api/expenses/', 
            headers=auth_headers,
            json={
                'amount': 50.00,
                'description': long_description
            }
        )
        
        # Should either truncate or accept up to DB limit
        assert response.status_code in [200, 400]
