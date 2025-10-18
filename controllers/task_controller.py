from extensions import db
from models.db_models import Task

def create_task(data):
    task = Task(
        title=data.get("title"),
        description=data.get("description"),
        completed=data.get("completed", False)
    )
    db.session.add(task)
    db.session.commit()
    return task

def update_task(task, data):
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    return task

def delete_task(task):
    db.session.delete(task)
    db.session.commit()
