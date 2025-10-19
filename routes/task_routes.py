from flask import Blueprint, request, jsonify
from models.db_models import DBService
from utils.auth_decorator import token_required, admin_required
from utils.logger import logger

task_routes = Blueprint("task_routes", __name__)

# === Get All Tasks ===
@task_routes.route("/tasks", methods=["GET"])
@token_required
def get_tasks():
    try:
        logger.info("Fetching list of all tasks")
        db = DBService.get_db()
        tasks = db.get_all_tasks()

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        start = (page - 1) * per_page
        end = start + per_page
        paginated_tasks = tasks[start:end]

        logger.info(f"Returning page {page} with {len(paginated_tasks)} tasks")
        return jsonify({
            "page": page,
            "per_page": per_page,
            "total": len(tasks),
            "tasks": paginated_tasks
        }), 200
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# === Get Task by ID ===
@task_routes.route("/tasks/<int:id>", methods=["GET"])
@token_required
def get_task(id):
    try:
        logger.info(f"Fetching task with id: {id}")
        db = DBService.get_db()
        task = db.get_task_by_id(id)
        if not task:
            logger.warning(f"Task not found: {id}")
            return jsonify({"error": "Task not found"}), 404
        return jsonify(task), 200
    except Exception as e:
        logger.error(f"Error fetching task {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# === Create a New Task ===
@task_routes.route("/create_tasks", methods=["POST"])
@token_required
@admin_required
def add_task():
    try:
        data = request.json
        title = data.get("title")
        description = data.get("description")
        completed = data.get("completed", False)

        if not title:
            logger.warning("Attempted to create task without title")
            return jsonify({"error": "Title is required"}), 400

        db = DBService.get_db()
        task_id = db.insert_task(title, description, completed)
        task = db.get_task_by_id(task_id)

        logger.info(f"Task created successfully with id: {task_id}")
        return jsonify(task), 201
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# === Update Task by ID ===
@task_routes.route("/tasks/<int:id>", methods=["PUT"])
@token_required
@admin_required
def edit_task(id):
    try:
        data = request.json
        db = DBService.get_db()
        task = db.get_task_by_id(id)
        if not task:
            logger.warning(f"Attempted to update non-existent task: {id}")
            return jsonify({"error": "Task not found"}), 404

        updated = db.update_task(
            task_id=id,
            title=data.get("title"),
            description=data.get("description"),
            completed=data.get("completed")
        )
        if not updated:
            logger.info(f"No changes made to task: {id}")
            return jsonify({"error": "Nothing to update"}), 400

        task = db.get_task_by_id(id)
        logger.info(f"Task updated successfully: {id}")
        return jsonify(task), 200
    except Exception as e:
        logger.error(f"Error updating task {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# === Delete Task by ID ===
@task_routes.route("/tasks/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def remove_task(id):
    try:
        db = DBService.get_db()
        task = db.get_task_by_id(id)
        if not task:
            logger.warning(f"Attempted to delete non-existent task: {id}")
            return jsonify({"error": "Task not found"}), 404

        db.delete_task(id)
        logger.info(f"Task deleted successfully: {id}")
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting task {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# === Get Completed Tasks ===
@task_routes.route("/tasks/completed", methods=["GET"])
@token_required
def get_completed_tasks():
    try:
        completed_param = request.args.get("completed", default="true").lower()
        if completed_param not in ["true", "false"]:
            logger.warning(f"Invalid completed query param: {completed_param}")
            return jsonify({"error": "Invalid value for 'completed'. Use true or false."}), 400

        completed_bool = completed_param == "true"

        db = DBService.get_db()
        tasks = db.get_all_tasks()
        filtered_tasks = [t for t in tasks if bool(t.get("completed")) == completed_bool]

        logger.info(f"Returning {len(filtered_tasks)} tasks with completed={completed_bool}")
        return jsonify(filtered_tasks), 200
    except Exception as e:
        logger.error(f"Error fetching completed tasks: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
