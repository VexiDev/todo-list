from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('home'))

    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/project/<int:id>', methods=['GET', 'POST'])
def project(id):
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status')
        new_task = Task(name=name, description=description, status=status, project_id=id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('project', id=id))

    project = Project.query.get_or_404(id)
    tasks = Task.query.filter_by(project_id=id).all()
    return render_template('project.html', project=project, tasks=tasks)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.name = request.form.get('name')
        project.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', project=project)

@app.route('/delete/<int:id>')
def delete(id):
    project = Project.query.get_or_404(id)
    for task in project.tasks:
        db.session.delete(task)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/task/<int:id>', methods=['POST'])
def task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.status = request.form.get('status')
        db.session.commit()
    return redirect(request.referrer)

@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.name = request.form.get('name')
        task.description = request.form.get('description')
        db.session.commit()
        return redirect(request.referrer)

    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(port=8080)
