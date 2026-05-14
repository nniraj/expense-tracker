from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Category

category_bp = Blueprint('categories', __name__)

# CREATE category
@category_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    data = request.json

    category = Category(
        name=data['name'],
        user_id=user_id
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({"msg": "Category created"}), 201


# GET all categories
@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    user_id = get_jwt_identity()

    categories = Category.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name
        } for c in categories
    ])


# UPDATE category
@category_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    category = Category.query.get(id)
    data = request.json

    category.name = data['name']
    db.session.commit()

    return jsonify({"msg": "Category updated"})


# DELETE category
@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    category = Category.query.get(id)

    db.session.delete(category)
    db.session.commit()

    return jsonify({"msg": "Category deleted"})