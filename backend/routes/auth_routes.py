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
        400: Missing required fields or email already exists
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate required fields
    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "username, email, and password are required"
        }), 400
    
    # Validate email format (basic check)
    if '@' not in email or '.' not in email:
        return jsonify({
            "success": False,
            "message": "Invalid email format"
        }), 400

    # check existing email
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 400
    
    # Check existing username
    existing_username = User.query.filter_by(username=username).first()
    
    if existing_username:
        return jsonify({
            "success": False,
            "message": "Username already exists"
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
        400: Missing required fields
        401: Invalid credentials (email not found or wrong password)
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    email = data.get('email')
    password = data.get('password')
    
    # Validate required fields
    if not email or not password:
        return jsonify({
            "success": False,
            "message": "email and password are required"
        }), 400

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