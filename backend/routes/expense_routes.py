from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.expense_model import Expense

expense_bp = Blueprint('expenses', __name__)

@expense_bp.route('/', methods=['POST'])
@jwt_required()
def create_expense():
    """
    Create a new expense for the authenticated user.
    
    Request body should contain:
        - amount (float): The expense amount
        - description (str): Description of the expense
        - category_id (int, optional): ID of the expense category
    
    Returns:
        JSON: Success message confirming expense was added
        
    Raises:
        401: If user is not authenticated
        400: If required fields are missing
    """
    user_id = int(get_jwt_identity())
    data = request.json

    expense = Expense(
        amount=data['amount'],
        description=data['description'],
        category_id=data.get('category_id'),
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()
    return jsonify({"msg": "Expense added"})


@expense_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    """
    Retrieve all expenses for the authenticated user.
    
    Returns:
        JSON: List of expenses with id, amount, and description
        
    Raises:
        401: If user is not authenticated
    """
    user_id = int(get_jwt_identity())
    expenses = Expense.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": e.id,
            "amount": e.amount,
            "description": e.description
        } for e in expenses
    ])


@expense_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_expense(id):
    """
    Update an existing expense by ID.
    
    Args:
        id (int): The expense ID to update
        
    Request body can contain (all optional):
        - amount (float): Updated expense amount
        - description (str): Updated expense description
        - category_id (int): Updated category ID
    
    Returns:
        JSON: Success message confirming update
        
    Raises:
        401: If user is not authenticated
        404: If expense ID not found
    """
    expense = Expense.query.get(id)
    data = request.json
    expense.amount = data.get('amount', expense.amount)
    expense.description = data.get('description', expense.description)
    expense.category_id = data.get('category_id', expense.category_id)
    db.session.commit()
    return jsonify({"msg": "Updated"})


@expense_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    """
    Delete an expense by ID.
    
    Args:
        id (int): The expense ID to delete
        
    Returns:
        JSON: Success message confirming deletion
        
    Raises:
        401: If user is not authenticated
        404: If expense ID not found
    """
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()

    return jsonify({"msg": "Deleted"})