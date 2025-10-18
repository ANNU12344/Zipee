from flask import Flask
from extensions import db, migrate
from routes.task_routes import task_routes
from routes.auth_routes import auth_routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger  # ✅ Import Swagger

def create_app():
    app = Flask(__name__)

    # === Configurations ===
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:dew%40123@localhost/tasks_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "aJf8sD92kLm3#pQrTz7yX!vB1n0WqE6"  # change in production
    app.config['SWAGGER'] = {
        'title': 'Task Management API',
        'uiversion': 3
    }


    

    # === Initialize extensions ===
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # === Initialize Swagger ===
    Swagger(app)  # ✅ This will serve Swagger UI at /apidocs

    # === Register blueprints ===
    app.register_blueprint(auth_routes)
    app.register_blueprint(task_routes)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
