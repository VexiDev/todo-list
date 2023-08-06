from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

status_order = ['Concept', 'Planned', 'Paused', 'Ongoing', 'Review', 'Completed','Cancelled']

@app.route('/add_task', methods=['POST'])
def add_task():
    # Load existing tasks
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

    # Get task details from the form
    task_name = request.form.get('name')
    task_description = request.form.get('description')
    task_status = request.form.get('status')

    # Add the new task
    tasks[task_status].append({
        'name': task_name,
        'description': task_description,
        'status': task_status
    })

    # Save tasks back to the file
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

    return redirect(url_for('task_list'))




def next_status(current_status):
    return status_order[(status_order.index(current_status) + 1) % len(status_order)]

def previous_status(current_status):
    return status_order[(status_order.index(current_status) - 1) % len(status_order)]


@app.route('/', methods=['GET', 'POST'])
def task_list():
    # Load existing tasks
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

    if request.method == 'POST':
        # Get task details from the form
        task_name = request.form.get('name')
        task_description = request.form.get('description')
        task_status = request.form.get('status')
        task_action = request.form.get('action')

        # Check if the task already exists
        for status, task_list in tasks.items():
            for i, task in enumerate(task_list):
                if task['name'] == task_name:
                    # The task exists, update its status
                    if task_action == 'increase':
                        task['status'] = next_status(task['status'])
                    elif task_action == 'decrease':
                        task['status'] = previous_status(task['status'])
                    task_list.pop(i)
                    tasks[task['status']].append(task)
                    break
            else:
                continue
            break
        else:
            # The task does not exist, add it
            if task_status:
                tasks[task_status].append({
                    'name': task_name,
                    'description': task_description,
                    'status': task_status
                })

        # Save tasks back to the file
        with open('tasks.json', 'w') as file:
            json.dump(tasks, file)

        return redirect(url_for('task_list'))

    else:
        return render_template('index.html', tasks=tasks, statuses=status_order)

if __name__ == '__main__':
    app.run(port=8081)
