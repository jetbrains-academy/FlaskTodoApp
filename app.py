from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'


# Update the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.task} in Project {self.project_id}>'


# Apply the changes to the database
with app.app_context():
    db.create_all()


# Create the database tables (ensure this block runs after adding the new models)
# Create the database tables
with app.app_context():
    db.create_all()


# Define the home route
@app.route('/')
def home():
    projects = Project.query.all()  # Get all projects
    return render_template('base.html', projects=projects)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add():
    task_content = request.form.get('task')
    if task_content:
        new_task = Todo(task=task_content, complete=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))

# Route to create a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    project_name = request.form.get('project_name')
    if project_name:
        new_project = Project(name=project_name)
        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for('home'))

# Route to update task status
@app.route('/update/<int:task_id>')
def update(task_id):
    task = Todo.query.get_or_404(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('home'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.get_or_404(task_id)
    project_id = task.project_id  # Retrieve the associated project ID
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('project_tasks', project_id=project_id))  # Redirect back to the project tasks page

@app.route('/project/<int:project_id>/add_task', methods=['POST'])
def add_task_to_project(project_id):
    # Get the project where the task will be added
    project = Project.query.get_or_404(project_id)
    task_content = request.form.get('task')

    if task_content:
        # Create a new task associated with the project
        new_task = Todo(task=task_content, complete=False, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('project_tasks', project_id=project_id))


@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)  # Get the project by ID or return 404

    # First, delete associated tasks
    Todo.query.filter_by(project_id=project_id).delete()

    # Then, delete the project itself
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('home'))  # Redirect to the home page

@app.route('/project/<int:project_id>')
def project_tasks(project_id):
    # Retrieve the project and its associated tasks
    project = Project.query.get_or_404(project_id)
    tasks = Todo.query.filter_by(project_id=project_id).all()

    return render_template('project_tasks.html', project=project, tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
