from functools import wraps
from flask import request, jsonify
import jwt
from models.db_models import DBService
from dotenv import load_dotenv
import os

# === Load environment variables ===
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Check JWT and attach user info
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid token format"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            db = DBService.get_db()
            user = db.get_user_by_id(data["user_id"])
            if not user:
                return jsonify({"error": "User not found"}), 401
            request.user = user  # attach user info to request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)
    return decorated

# Only admin users
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not getattr(request, "user", None):
            return jsonify({"error": "User not authenticated"}), 401
        if request.user["role"] != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated
