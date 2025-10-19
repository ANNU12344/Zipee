from flask import request, jsonify
from models.db_models import DBService
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from dotenv import load_dotenv
from models.db_models import DBService
import jwt
import os

# === Load environment variables ===
load_dotenv()
jwt_secret = os.getenv("JWT_SECRET_KEY")


def register_user():
    db = DBService.get_db()
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")  # default role = 'user'

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Check if user exists
    existing_user = db.get_user_by_email(email)
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # Insert user with role
    success, user_id = db.insert_user(email, password, role=role)
    if not success:
        return jsonify({"message": "Failed to register user"}), 500

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201


# ===== Login User =====
def login_user():
    db = DBService.get_db()
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    # Get user by email
    user = db.get_user_by_email(email)
    if not user or not db.check_user_password(email, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Create JWT payload
    payload = {
        "user_id": user["id"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=12)  # token expires in 12 hours
    }

    # Encode JWT
    access_token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    return jsonify({"access_token": access_token}), 200
