from flask import request, jsonify
from models.db_models import DBService
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os
from utils.logger import logger  # ✅ Import logger

# === Load environment variables ===
load_dotenv()
jwt_secret = os.getenv("JWT_SECRET_KEY")


def register_user():
    try:
        data = request.json
        if not data:
            logger.warning("Empty registration request body")
            return jsonify({"message": "Request body is empty"}), 400

        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")  # default role = 'user'

        logger.info(f"Attempting to register user with email: {email}")

        if not email or not password:
            logger.warning("Email or password missing in registration request")
            return jsonify({"message": "Email and password are required"}), 400

        try:
            db = DBService.get_db()
        except Exception as db_err:
            logger.exception(f"Failed to connect to DB: {db_err}")
            return jsonify({"message": "Database connection error"}), 500

        try:
            # Check if user exists
            existing_user = db.get_user_by_email(email)
            if existing_user:
                logger.warning(f"Registration failed: Email already registered - {email}")
                return jsonify({"message": "Email already registered"}), 400
        except Exception as get_user_err:
            logger.exception(f"Error checking existing user: {get_user_err}")
            return jsonify({"message": "Database error"}), 500

        try:
            # Insert user with role
            success, user_id = db.insert_user(email, password, role=role)
            if not success:
                logger.error(f"Failed to insert user into database: {email}")
                return jsonify({"message": "Failed to register user"}), 500
        except Exception as insert_err:
            logger.exception(f"Error inserting user: {insert_err}")
            return jsonify({"message": "Database error"}), 500

        logger.info(f"User registered successfully: {email} with role {role}")
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

    except Exception as e:
        logger.exception(f"Exception during user registration: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500


def login_user():
    try:
        data = request.json
        if not data:
            logger.warning("Empty login request body")
            return jsonify({"message": "Request body is empty"}), 400

        email = data.get("email")
        password = data.get("password")

        logger.info(f"Login attempt for email: {email}")

        if not email or not password:
            logger.warning("Email or password missing in login request")
            return jsonify({"message": "Email and password required"}), 400

        try:
            db = DBService.get_db()
        except Exception as db_err:
            logger.exception(f"Failed to connect to DB: {db_err}")
            return jsonify({"message": "Database connection error"}), 500

        try:
            user = db.get_user_by_email(email)
            if not user:
                logger.warning(f"User not found: {email}")
                return jsonify({"message": "Invalid credentials"}), 401

            if not db.check_user_password(email, password):
                logger.warning(f"Invalid password attempt for email: {email}")
                return jsonify({"message": "Invalid credentials"}), 401
        except Exception as db_check_err:
            logger.exception(f"Error checking user credentials: {db_check_err}")
            return jsonify({"message": "Database error"}), 500

        try:
            # Create JWT payload
            payload = {
                "user_id": user["id"],
                "role": user["role"],
                "exp": datetime.utcnow() + timedelta(hours=12)
            }

            access_token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        except Exception as jwt_err:
            logger.exception(f"JWT encoding failed: {jwt_err}")
            return jsonify({"message": "Failed to generate access token"}), 500

        logger.info(f"Login successful for email: {email}")
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        logger.exception(f"Exception during user login: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500
