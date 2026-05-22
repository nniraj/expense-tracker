"""
Tests for category management routes (CRUD operations).
"""
import pytest
from models.category_model import Category


class TestCreateCategory:
    """Test suite for creating categories."""

    def test_create_category_success(self, client, auth_headers):
        """Test successful category creation."""
        response = client.post('/api/categories/', 
            headers=auth_headers,
            json={
                'name': 'Groceries'
            }
        )
        
        assert response.status_code == 201
        assert 'Category created' in response.json.get('msg', '')

    def test_create_category_missing_name(self, client, auth_headers):
        """Test creating category fails without name."""
        response = client.post('/api/categories/', 
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code in [400, 500]

    def test_create_category_requires_auth(self, client):
        """Test that creating category requires authentication."""
        response = client.post('/api/categories/', 
            json={'name': 'Unauthorized'}
        )
        
        assert response.status_code == 401

    def test_create_category_invalid_token(self, client):
        """Test that invalid token is rejected."""
        headers = {
            'Authorization': 'Bearer invalid.token.here',
            'Content-Type': 'application/json'
        }
        response = client.post('/api/categories/', 
            headers=headers,
            json={'name': 'Groceries'}
        )
        
        assert response.status_code == 401

    def test_create_category_stores_correctly(self, client, auth_headers, app):
        """Test that category is stored in database."""
        client.post('/api/categories/', 
            headers=auth_headers,
            json={'name': 'Dining'}
        )
        
        with app.app_context():
            category = Category.query.filter_by(name='Dining').first()
            assert category is not None

    def test_create_multiple_categories(self, client, auth_headers, app):
        """Test creating multiple categories."""
        names = ['Groceries', 'Transport', 'Entertainment']
        
        for name in names:
            response = client.post('/api/categories/', 
                headers=auth_headers,
                json={'name': name}
            )
            assert response.status_code == 201
        
        with app.app_context():
            count = Category.query.filter(Category.name.in_(names)).count()
            assert count >= 3  # At least the new ones (might have fixtures)


class TestGetCategories:
    """Test suite for retrieving categories."""

    def test_get_categories_success(self, client, auth_headers, test_categories):
        """Test successful retrieval of categories."""
        response = client.get('/api/categories/', headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json, list)
        # Should have at least the test categories
        assert len(response.json) >= 4

    def test_get_categories_empty(self, client, auth_headers):
        """Test getting categories when none exist."""
        response = client.get('/api/categories/', headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_get_categories_requires_auth(self, client):
        """Test that getting categories requires authentication."""
        response = client.get('/api/categories/')
        
        assert response.status_code == 401

    def test_get_categories_invalid_token(self, client):
        """Test that invalid token is rejected."""
        headers = {'Authorization': 'Bearer invalid.token'}
        response = client.get('/api/categories/', headers=headers)
        
        assert response.status_code == 401

    def test_get_categories_includes_all_fields(self, client, auth_headers, test_categories):
        """Test that category response includes all required fields."""
        response = client.get('/api/categories/', headers=auth_headers)
        
        if response.json:
            category = response.json[0]
            assert 'id' in category
            assert 'name' in category

    def test_get_categories_returns_all_users_can_access(self, client, auth_headers_2, test_categories):
        """Test that all users can access all categories (shared categories)."""
        response = client.get('/api/categories/', headers=auth_headers_2)
        
        assert response.status_code == 200
        # Should return the test categories even for different user
        assert len(response.json) >= 4

    def test_get_categories_contains_created_categories(self, client, auth_headers):
        """Test that created categories appear in get response."""
        # Create a category
        client.post('/api/categories/', 
            headers=auth_headers,
            json={'name': 'NewCategory123'}
        )
        
        # Retrieve all
        response = client.get('/api/categories/', headers=auth_headers)
        names = [cat['name'] for cat in response.json]
        
        assert 'NewCategory123' in names


class TestUpdateCategory:
    """Test suite for updating categories."""

    def test_update_category_success(self, client, auth_headers, test_categories):
        """Test successful category update."""
        category_id = test_categories[0].id
        response = client.put(f'/api/categories/{category_id}', 
            headers=auth_headers,
            json={'name': 'UpdatedFood'}
        )
        
        assert response.status_code == 200
        assert 'Category updated' in response.json.get('msg', '')

    def test_update_category_missing_name(self, client, auth_headers, test_categories):
        """Test updating category fails without name."""
        category_id = test_categories[0].id
        response = client.put(f'/api/categories/{category_id}', 
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code in [400, 500]

    def test_update_category_not_found(self, client, auth_headers):
        """Test updating non-existent category."""
        response = client.put('/api/categories/99999', 
            headers=auth_headers,
            json={'name': 'Ghost'}
        )
        
        assert response.status_code == 404

    def test_update_category_requires_auth(self, client, test_categories):
        """Test that updating category requires authentication."""
        response = client.put(f'/api/categories/{test_categories[0].id}', 
            json={'name': 'Unauthorized'}
        )
        
        assert response.status_code == 401

    def test_update_category_verifies_changes(self, client, auth_headers, test_categories, app):
        """Test that category update is reflected in database."""
        category_id = test_categories[0].id
        client.put(f'/api/categories/{category_id}', 
            headers=auth_headers,
            json={'name': 'VerifiedUpdate'}
        )
        
        with app.app_context():
            category = Category.query.get(category_id)
            assert category.name == 'VerifiedUpdate'


class TestDeleteCategory:
    """Test suite for deleting categories."""

    def test_delete_category_success(self, client, auth_headers, test_categories):
        """Test successful category deletion."""
        category_id = test_categories[0].id
        response = client.delete(f'/api/categories/{category_id}', 
            headers=auth_headers
        )
        
        assert response.status_code == 200

    def test_delete_category_not_found(self, client, auth_headers):
        """Test deleting non-existent category."""
        response = client.delete('/api/categories/99999', 
            headers=auth_headers
        )
        
        assert response.status_code == 404

    def test_delete_category_requires_auth(self, client, test_categories):
        """Test that deleting category requires authentication."""
        response = client.delete(f'/api/categories/{test_categories[0].id}')
        
        assert response.status_code == 401

    def test_delete_category_removes_from_database(self, client, auth_headers, test_categories, app):
        """Test that deleted category is removed from database."""
        category_id = test_categories[0].id
        client.delete(f'/api/categories/{category_id}', headers=auth_headers)
        
        with app.app_context():
            category = Category.query.get(category_id)
            assert category is None

    def test_delete_category_verify_count(self, client, auth_headers, test_categories):
        """Test that deleting reduces category count."""
        # Get initial count
        response1 = client.get('/api/categories/', headers=auth_headers)
        initial_count = len(response1.json)
        
        # Delete one
        client.delete(f'/api/categories/{test_categories[0].id}', headers=auth_headers)
        
        # Get new count
        response2 = client.get('/api/categories/', headers=auth_headers)
        assert len(response2.json) == initial_count - 1


class TestCategoryValidation:
    """Test suite for category data validation."""

    def test_category_long_name(self, client, auth_headers):
        """Test handling of long category name."""
        long_name = 'A' * 200
        response = client.post('/api/categories/', 
            headers=auth_headers,
            json={'name': long_name}
        )
        
        # Should either truncate or accept up to DB limit
        assert response.status_code in [201, 400]

    def test_category_special_characters(self, client, auth_headers):
        """Test category names with special characters."""
        response = client.post('/api/categories/', 
            headers=auth_headers,
            json={'name': 'Food & Dining!@#$%'}
        )
        
        assert response.status_code == 201

    def test_category_unicode_characters(self, client, auth_headers):
        """Test category names with unicode characters."""
        response = client.post('/api/categories/', 
            headers=auth_headers,
            json={'name': '食料品 (Groceries)'}
        )
        
        assert response.status_code == 201

    def test_category_whitespace_handling(self, client, auth_headers):
        """Test category names with extra whitespace."""
        response = client.post('/api/categories/', 
            headers=auth_headers,
            json={'name': '  Spaced Name  '}
        )
        
        assert response.status_code == 201
