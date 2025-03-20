from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Constants for configuration
DATABASE_URI = 'sqlite:///todo.db'
TRACK_MODIFICATIONS = False

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TRACK_MODIFICATIONS
db = SQLAlchemy(app)


# Models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.task} in Project {self.project_id}>'


# Extracted function: Initializes the database
def init_db():
    with app.app_context():
        db.create_all()


# Initialize database
init_db()


# Routes
@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('base.html', projects=projects)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        new_task = Todo(task=task_content, complete=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/create_project', methods=['POST'])
def create_project():
    project_name = request.form.get('project_name')
    if project_name:
        new_project = Project(name=project_name)
        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/toggle_task_complete/<int:task_id>')
def toggle_task_complete(task_id):
    task = Todo.query.get_or_404(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('project_tasks', project_id=task.project_id))


@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('project_tasks', project_id=task.project_id))


@app.route('/project/<int:project_id>/add_task', methods=['POST'])
def add_project_task(project_id):
    project = Project.query.get_or_404(project_id)
    task_content = request.form.get('task')
    if task_content:
        new_task = Todo(task=task_content, complete=False, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('project_tasks', project_id=project_id))


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    Todo.query.filter_by(project_id=project_id).delete()  # Cascade delete tasks
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/project/<int:project_id>')
def project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Todo.query.filter_by(project_id=project_id).all()
    return render_template('project_tasks.html', project=project, tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
