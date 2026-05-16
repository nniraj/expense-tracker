from flask import Blueprint, request, jsonify
from models.user_models import User
from extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)


# REGISTER API
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user account.
    
    Request body should contain:
        - username (str): Unique username for the account
        - email (str): Unique email address
        - password (str): Account password (will be hashed)
    
    Returns:
        JSON: Success message with user creation confirmation
        
    Status codes:
        201: User registered successfully
        400: Email already exists
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # check existing email
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 400

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    }), 201


# LOGIN API
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT access token.
    
    Request body should contain:
        - email (str): User's email address
        - password (str): User's password
    
    Returns:
        JSON: Access token and user details (id, username, email)
        
    Status codes:
        200: Login successful, token returned
        401: Invalid credentials (email not found or wrong password)
    """
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):

        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    })