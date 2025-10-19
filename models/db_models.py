# from extensions import db
# from datetime import datetime
# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()

# class Task(db.Model):
#     __tablename__ = "task"
    
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     completed = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "description": self.description,
#             "completed": self.completed,
#             "created_at": self.created_at,
#             "updated_at": self.updated_at
#         }



# class User(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def set_password(self, password):
#         """Hashes and sets the user's password."""
#         self.password = bcrypt.generate_password_hash(password).decode('utf-8')

#     def check_password(self, password):
#         """Checks a plaintext password against the hashed one."""
#         return bcrypt.check_password_hash(self.password, password)

#     def to_dict(self):
#         """Return a dictionary representation without the password."""
#         return {
#             "id": self.id,
#             "username": self.username,
#             "email": self.email,
#             "created_at": self.created_at.isoformat()
#         }



import mysql.connector
from mysql.connector import Error
from datetime import datetime
from passlib.hash import bcrypt
from fastapi import FastAPI, HTTPException
class DBService:
    db = None

    @classmethod
    def init(cls):
        cls.db = MySQLDatabase(
            host="localhost",
            user="root",
            password="dew@123",
            database="tasks_db"
        )
        cls.db.connect()
        cls.db.create_user_table()
        cls.db.create_task_table()

    @classmethod
    def get_db(cls):
        return cls.db




class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a MySQL connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("✅ Connected to MySQL database")
        except Error as e:
            print("❌ Error while connecting to MySQL:", e)

    # ===== Table Creation =====
    def create_task_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS task (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("🗃️ Table 'task' created successfully")

    def create_user_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("🗃️ Table 'users' created successfully")


    # ===== Task CRUD Operations =====
    def insert_task(self, title, description=None, completed=False):
        insert_query = """
        INSERT INTO task (title, description, completed)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(insert_query, (title, description, completed))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_tasks(self):
        self.cursor.execute("SELECT * FROM task")
        return self.cursor.fetchall()

    def get_task_by_id(self, task_id):
        self.cursor.execute("SELECT * FROM task WHERE id = %s", (task_id,))
        return self.cursor.fetchone()

    def update_task(self, task_id, title=None, description=None, completed=None):
        update_fields, values = [], []

        if title is not None:
            update_fields.append("title = %s")
            values.append(title)
        if description is not None:
            update_fields.append("description = %s")
            values.append(description)
        if completed is not None:
            update_fields.append("completed = %s")
            values.append(completed)

        if not update_fields:
            return False

        values.append(task_id)
        update_query = f"UPDATE task SET {', '.join(update_fields)}, updated_at = NOW() WHERE id = %s"
        self.cursor.execute(update_query, tuple(values))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM task WHERE id = %s", (task_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    # ===== User CRUD =====
    def insert_user(self, email, password, role="user"):
    # Check if email exists
        self.cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
        if self.cursor.fetchone():
            return False, "Email already registered"

        # Hash the password
        hashed = bcrypt.hash(password)

        # Insert user
        insert_query = "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)"
        self.cursor.execute(insert_query, (email, hashed, role))
        self.connection.commit()

        return True, self.cursor.lastrowid
    

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s LIMIT 1", (user_id,))
        return self.cursor.fetchone()



    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
        return self.cursor.fetchone()

    def check_user_password(self, email, password):
        user = self.get_user_by_email(email)
        if not user:
            return False
        return bcrypt.verify(password, user["password"])

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔒 MySQL connection closed")









