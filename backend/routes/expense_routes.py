from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Expense

expense_bp = Blueprint('expenses', __name__)

@expense_bp.route('/', methods=['POST'])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    data = request.json

    expense = Expense(
        amount=data['amount'],
        description=data['description'],
        category_id=data['category_id'],
        user_id=user_id
    )

    db.session.add(expense)
    db.session.commit()
    return jsonify({"msg": "Expense added"})


@expense_bp.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
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
    expense = Expense.query.get(id)
    data = request.json

    expense.amount = data['amount']
    expense.description = data['description']

    db.session.commit()
    return jsonify({"msg": "Updated"})


@expense_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()

    return jsonify({"msg": "Deleted"})