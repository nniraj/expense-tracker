from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.category_model import Category

category_bp = Blueprint('categories', __name__)

# CREATE category
@category_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    """
    Create a new expense category.
    
    Request body should contain:
        - name (str): The category name
    
    Returns:
        JSON: Success message confirming category was created
        
    Status codes:
        201: Category created successfully
        401: If user is not authenticated
        400: If name is missing
    """
    data = request.json

    category = Category(
        name=data['name']
    )

    db.session.add(category)
    db.session.commit()

    return jsonify({"msg": "Category created"}), 201


# GET all categories
@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Retrieve all expense categories.
    
    Returns:
        JSON: List of all categories with id and name
        
    Status codes:
        200: Categories retrieved successfully
        401: If user is not authenticated
    """
    categories = Category.query.all()

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
    """
    Update an existing category by ID.
    
    Args:
        id (int): The category ID to update
        
    Request body should contain:
        - name (str): Updated category name
    
    Returns:
        JSON: Success message confirming update
        
    Status codes:
        200: Category updated successfully
        401: If user is not authenticated
        404: If category ID not found
    """
    category = Category.query.get(id)
    data = request.json

    category.name = data['name']
    db.session.commit()

    return jsonify({"msg": "Category updated"})


# DELETE category
@category_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    """
    Delete a category by ID.
    
    Args:
        id (int): The category ID to delete
        
    Returns:
        JSON: Success message confirming deletion
        
    Status codes:
        200: Category deleted successfully
        401: If user is not authenticated
        404: If category ID not found
    """
    category = Category.query.get(id)

    db.session.delete(category)
    db.session.commit()

    return jsonify({"msg": "Category deleted"})