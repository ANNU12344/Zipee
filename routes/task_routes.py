from flask import Blueprint, request, jsonify
from models.db_models import Task
from controllers.task_controller import create_task, update_task, delete_task

task_routes = Blueprint("task_routes", __name__)

@task_routes.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Get All Tasks
    ---
    tags:
      - Tasks
    responses:
      200:
        description: List of tasks
    """
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])


@task_routes.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    """
    Get Task by ID
    ---
    tags:
      - Tasks
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Task details
      404:
        description: Task not found
    """
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())


@task_routes.route("/tasks", methods=["POST"])
def add_task():
    """
    Create a New Task
    ---
    tags:
      - Tasks
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Buy groceries"
            description:
              type: string
              example: "Milk, Eggs, Bread"
            completed:
              type: boolean
              example: false
    responses:
      201:
        description: Task created successfully
    """
    data = request.json
    task = create_task(data)
    return jsonify(task.to_dict()), 201


@task_routes.route("/tasks/<int:id>", methods=["PUT"])
def edit_task(id):
    """
    Update Task by ID
    ---
    tags:
      - Tasks
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the task
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Buy groceries updated"
            description:
              type: string
              example: "Milk, Eggs, Bread, Butter"
            completed:
              type: boolean
              example: true
    responses:
      200:
        description: Task updated successfully
      404:
        description: Task not found
    """
    task = Task.query.get_or_404(id)
    data = request.json
    task = update_task(task, data)
    return jsonify(task.to_dict())


@task_routes.route("/tasks/<int:id>", methods=["DELETE"])
def remove_task(id):
    """
    Delete Task by ID
    ---
    tags:
      - Tasks
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the task
    responses:
      200:
        description: Task deleted successfully
      404:
        description: Task not found
    """
    task = Task.query.get_or_404(id)
    delete_task(task)
    return jsonify({"message": "Task deleted successfully."})
