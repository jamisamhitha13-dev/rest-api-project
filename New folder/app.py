
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Temporary storage for tasks
tasks = []
next_id = 1


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# GET: Retrieve all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


# POST: Add a new task
@app.route("/api/tasks", methods=["POST"])
def add_task():
    global next_id

    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


# PUT: Update task completion status
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = data.get(
                "completed", not task["completed"]
            )
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404


# DELETE: Delete a task
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted successfully"})

    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)