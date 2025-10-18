from flask import Blueprint
from controllers.auth_controller import register_user, login_user

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/register", methods=["POST"])
def register():
    """
    User Registration
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: "john_doe"
            email:
              type: string
              example: "john@example.com"
            password:
              type: string
              example: "mypassword123"
    responses:
      201:
        description: User registered successfully
      400:
        description: Email already exists
    """
    return register_user()


@auth_routes.route("/login", methods=["POST"])
def login():
    """
    User Login
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "john@example.com"
            password:
              type: string
              example: "mypassword123"
    responses:
      200:
        description: Login successful, returns access_token
      401:
        description: Invalid credentials
    """
    return login_user()
