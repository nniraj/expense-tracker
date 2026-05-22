"""
Expense Tracker Backend Test Suite

This package contains all pytest tests for the expense tracker backend API.

Test files:
- test_auth_routes.py: Authentication and user management tests
- test_expense_routes.py: Expense CRUD operation tests
- test_category_routes.py: Category CRUD operation tests
- test_jwt_auth.py: JWT authentication and authorization tests
- test_models.py: Database model tests

Fixtures:
- conftest.py: Shared fixtures and test configuration

Run all tests:
    pytest

Run specific test file:
    pytest tests/test_auth_routes.py

Run with coverage:
    pytest --cov=routes --cov=models --cov-report=html

For more information, see TESTS_README.md
"""
