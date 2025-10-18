from flask import Flask
from extensions import db, migrate
from routes.task_routes import task_routes
from routes.auth_routes import auth_routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv
import os

# === Load .env file ===
load_dotenv()

def create_app():
    app = Flask(__name__)

    # === Configurations ===
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    jwt_secret = os.getenv("JWT_SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = jwt_secret
    app.config['SWAGGER'] = {
        'title': 'Task Management API',
        'uiversion': 3
    }

    # === Initialize extensions ===
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # === Initialize Swagger ===
    Swagger(app)

    # === Register blueprints ===
    app.register_blueprint(auth_routes)
    app.register_blueprint(task_routes)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
