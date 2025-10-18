from flask import request, jsonify
from extensions import db, bcrypt
from sqlalchemy import text
from flask_jwt_extended import create_access_token

# 1️⃣ Create users table if not exists
def create_users_table():
    print("*********************************************")
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    with db.engine.begin() as conn:  # use begin() to auto-commit
        conn.execute(text(query))
    print("Users table ensured.")

# 2️⃣ Register user
def register_user():
    create_users_table()  # ensure table exists
    data = request.json
    email = data["email"]

    # Check if user exists
    query = "SELECT * FROM users WHERE email = :email LIMIT 1;"
    with db.engine.connect() as conn:
        result = conn.execute(text(query), {"email": email}).fetchone()

    if result:
        return jsonify({"message": "Email already registered"}), 400

    hashed = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    insert_query = """
    INSERT INTO users (username, email, password) 
    VALUES (:username, :email, :password)
    """
    with db.engine.begin() as conn:  # begin() will commit automatically
        conn.execute(text(insert_query), {"username": data["username"], "email": email, "password": hashed})

    return jsonify({"message": "User registered successfully"}), 201

# 3️⃣ Login user
def login_user():
    data = request.json
    email = data["email"]
    password = data["password"]

    query = "SELECT * FROM users WHERE email = :email LIMIT 1;"
    with db.engine.connect() as conn:
        result = conn.execute(text(query), {"email": email}).fetchone()

    if not result or not bcrypt.check_password_hash(result.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=result.id)
    return jsonify({"access_token": access_token})
