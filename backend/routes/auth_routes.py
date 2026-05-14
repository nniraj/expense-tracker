from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import create_access_token
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

    user = User(username=data['username'], password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.checkpw(data['password'].encode(), user.password):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)

    return jsonify({"msg": "Invalid credentials"}), 401