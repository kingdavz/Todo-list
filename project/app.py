#!/usr/bin/python
"""a module that handles the to do list"""


from flask import Flask, render_template, request
from util import load_tasks, save_tasks

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():

    res = {"message": ""}
    tasks = load_tasks()

    if request.method == 'POST':

        action = request.form.get("action")

        if action == "add":
            task_text = request.form.get('task')

            if task_text:
                tasks.append({
                    "text": task_text,
                    "completed": False
                })
                save_tasks(tasks)
                res["message"] = "Task added successfully"

        elif action == "edit":
            task_id = int(request.form.get("task_id"))
            new_task = request.form.get("task")

            if new_task and 0 <= task_id < len(tasks):
                tasks[task_id]["text"] = new_task
                save_tasks(tasks)
                res["message"] = "Task updated"

        elif action == "delete":
            task_id = int(request.form.get("task_id"))

            if 0 <= task_id < len(tasks):
                tasks.pop(task_id)
                save_tasks(tasks)
                res["message"] = "Task deleted"

        elif action == "toggle":
            task_id = int(request.form.get("task_id"))

            if 0 <= task_id < len(tasks):
                tasks[task_id]["completed"] = not tasks[task_id]["completed"]
                save_tasks(tasks)
                res["message"] = "Task status updated"

        tasks = load_tasks()

    return render_template('index.html', tasks=tasks, res=res)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)