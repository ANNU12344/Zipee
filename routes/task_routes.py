from flask import Blueprint, request, jsonify
from models.db_models import DBService
from utils.auth_decorator import token_required, admin_required
from utils.logger import logger

task_routes = Blueprint("task_routes", __name__)


# Routes to get the lsit of all the tasks 
@task_routes.route("/tasks", methods=["GET"])
@token_required
def get_tasks():
    logger.info(f"Get list of all the task")
    db = DBService.get_db()  # db connection 
    tasks = db.get_all_tasks() # call the get_all_task function to get the list of the all the task return the list 

    # Get query params for pagination
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    # Calculate start and end index
    start = (page - 1) * per_page
    end = start + per_page

    paginated_tasks = tasks[start:end]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": len(tasks),
        "tasks": paginated_tasks
    }), 200

# === Get Task by ID ===
@task_routes.route("/tasks/<int:id>", methods=["GET"])
@token_required  # both admin & user
def get_task(id):
    db = DBService.get_db()
    task = db.get_task_by_id(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200

# === Create a New Task ===
@task_routes.route("/create_tasks", methods=["POST"])
@token_required
@admin_required  # only admin
def add_task():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed", False)

    if not title:
        return jsonify({"error": "Title is required"}), 400

    db = DBService.get_db()
    task_id = db.insert_task(title, description, completed)
    task = db.get_task_by_id(task_id)
    return jsonify(task), 201

# === Update Task by ID ===
@task_routes.route("/tasks/<int:id>", methods=["PUT"])
@token_required
@admin_required  # only admin
def edit_task(id):
    data = request.json
    db = DBService.get_db()
    task = db.get_task_by_id(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    updated = db.update_task(
        task_id=id,
        title=data.get("title"),
        description=data.get("description"),
        completed=data.get("completed")
    )
    if not updated:
        return jsonify({"error": "Nothing to update"}), 400

    task = db.get_task_by_id(id)
    return jsonify(task), 200

# === Delete Task by ID ===
@task_routes.route("/tasks/<int:id>", methods=["DELETE"])
@token_required
@admin_required  # only admin
def remove_task(id):
    db = DBService.get_db()
    task = db.get_task_by_id(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.delete_task(id)
    return jsonify({"message": "Task deleted successfully"}), 200

# === Get Completed Tasks ===
@task_routes.route("/tasks/completed", methods=["GET"])
@token_required  # both admin & user
def get_completed_tasks():
    completed_param = request.args.get("completed", default="true").lower()
    
    if completed_param not in ["true", "false"]:
        return jsonify({"error": "Invalid value for 'completed'. Use true or false."}), 400

    completed_bool = completed_param == "true"

    db = DBService.get_db()
    tasks = db.get_all_tasks()
    filtered_tasks = [t for t in tasks if bool(t.get("completed")) == completed_bool]

    return jsonify(filtered_tasks), 200
