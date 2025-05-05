# backend/controllers/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already taken"}), 400
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        is_admin=data.get('is_admin', False)
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user.to_dict()), 200

# Endpoint untuk keperluan demo - Menambahkan user demo jika belum ada
@auth_bp.route('/create-demo-users', methods=['GET'])
def create_demo_users():
    # Cek apakah ada user admin
    admin = User.query.filter_by(email='admin@meetnote.com').first()
    if not admin:
        admin = User(
            username='Admin',
            email='admin@meetnote.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Cek apakah ada user biasa
    user = User.query.filter_by(email='user@meetnote.com').first()
    if not user:
        user = User(
            username='User',
            email='user@meetnote.com',
            is_admin=False
        )
        user.set_password('user123')
        db.session.add(user)
    
    db.session.commit()
    
    return jsonify({"message": "Demo users created successfully"}), 201