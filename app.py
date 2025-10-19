from flask import Flask
from extensions import db, migrate
from routes.task_routes import task_routes
from routes.auth_routes import auth_routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv
from models.db_models import DBService
import os

# === Load environment variables ===
load_dotenv()


def create_app():
    app = Flask(__name__)

    # === Configurations ===
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    #

    print(f"Username: {db_username}, Password: {db_password}, Host: {db_host}, DB: {db_name}")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    

    # === Initialize Extensions ===
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    Swagger(app)

    # === Register Blueprints ===
    app.register_blueprint(auth_routes)
    app.register_blueprint(task_routes)


    # === Lifecycle Hooks ===
    with app.app_context():
        print("🚀 Starting up DBService...")
        DBService.init()

    return app


# === Create app instance ===
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
