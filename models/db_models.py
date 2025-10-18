from extensions import db
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Task(db.Model):
    __tablename__ = "task"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }



class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks a plaintext password against the hashed one."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Return a dictionary representation without the password."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }





# import mysql.connector
# from mysql.connector import Error
# from datetime import datetime
# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt()


# class MySQLDatabase:
#     def __init__(self, host, user, password, database):
#         self.host = host
#         self.user = user
#         self.password = password
#         self.database = database
#         try:
#             self.connection = mysql.connector.connect(
#                 host=self.host,
#                 user=self.user,
#                 password=self.password,
#                 database=self.database
#             )
#             if self.connection.is_connected():
#                 self.cursor = self.connection.cursor(dictionary=True)
#                 print("Connected to MySQL database")
#         except Error as e:
#             print("Error while connecting to MySQL", e)

#     # ===== Table Creation =====
#     def create_task_table(self):
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS task (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             title VARCHAR(255) NOT NULL,
#             description TEXT,
#             completed BOOLEAN DEFAULT FALSE,
#             created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#             updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         )
#         """
#         self.cursor.execute(create_table_query)
#         print("Table 'task' created successfully")

#     def create_user_table(self):
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS users (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             username VARCHAR(50) UNIQUE NOT NULL,
#             email VARCHAR(100) UNIQUE NOT NULL,
#             password VARCHAR(200) NOT NULL,
#             created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#             updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#         )
#         """
#         self.cursor.execute(create_table_query)
#         print("Table 'users' created successfully")

#     # ===== Task CRUD Operations =====
#     def insert_task(self, title, description=None, completed=False):
#         insert_query = """
#         INSERT INTO task (title, description, completed)
#         VALUES (%s, %s, %s)
#         """
#         self.cursor.execute(insert_query, (title, description, completed))
#         self.connection.commit()
#         print("Task inserted successfully with ID:", self.cursor.lastrowid)
#         return self.cursor.lastrowid

#     def get_all_tasks(self):
#         select_query = "SELECT * FROM task"
#         self.cursor.execute(select_query)
#         tasks = self.cursor.fetchall()
#         return tasks

#     def get_task_by_id(self, task_id):
#         select_query = "SELECT * FROM task WHERE id = %s"
#         self.cursor.execute(select_query, (task_id,))
#         task = self.cursor.fetchone()
#         return task

#     def update_task(self, task_id, title=None, description=None, completed=None):
#         update_fields = []
#         values = []

#         if title is not None:
#             update_fields.append("title = %s")
#             values.append(title)
#         if description is not None:
#             update_fields.append("description = %s")
#             values.append(description)
#         if completed is not None:
#             update_fields.append("completed = %s")
#             values.append(completed)

#         if not update_fields:
#             return False  # Nothing to update

#         values.append(task_id)
#         update_query = f"UPDATE task SET {', '.join(update_fields)}, updated_at = NOW() WHERE id = %s"
#         self.cursor.execute(update_query, tuple(values))
#         self.connection.commit()
#         return self.cursor.rowcount > 0

#     def delete_task(self, task_id):
#         delete_query = "DELETE FROM task WHERE id = %s"
#         self.cursor.execute(delete_query, (task_id,))
#         self.connection.commit()
#         return self.cursor.rowcount > 0

#     # ===== Close Connection =====
#     def close(self):
#         if self.connection.is_connected():
#             self.cursor.close()
#             self.connection.close()
#             print("MySQL connection closed")
    



#     from flask_bcrypt import Bcrypt


#     def insert_user(self, username, email, password):
#         # Check if email exists
#         self.cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
#         if self.cursor.fetchone():
#             return False, "Email already registered"

#         hashed = bcrypt.generate_password_hash(password).decode('utf-8')
#         insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
#         self.cursor.execute(insert_query, (username, email, hashed))
#         self.connection.commit()
#         return True, self.cursor.lastrowid

#     def get_user_by_email(self, email):
#         self.cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
#         return self.cursor.fetchone()

#     def check_user_password(self, email, password):
#         user = self.get_user_by_email(email)
#         if not user:
#             return False
#         return bcrypt.check_password_hash(user["password"], password)









