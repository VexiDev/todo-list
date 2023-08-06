from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

status_list = ['Concept', 'Planned', 'Ongoing','Core Features Implemented', 'Completed', 'Paused']

def add_task(name, description, status):
    # Load existing tasks
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

    # Add new task
    tasks.append({
        'name': name,
        'description': description,
        'status': status
    })

    # Save tasks back to the file
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)


@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
    except:
        tasks = []

    if request.method == 'POST':
        for task in tasks:
            if task['name'] == request.form.get('name'):
                current_status = task['status']
                current_status_index = status_list.index(current_status)
                next_status_index = (current_status_index + 1) % len(status_list)
                task['status'] = status_list[next_status_index]
                break

        with open('tasks.json', 'w') as f:
            json.dump(tasks, f)

        return redirect(url_for('home'))

    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(port=8080)
