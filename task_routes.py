from flask import request, redirect, url_for, render_template
from models import Task, Project
from database_initialization import db
from routes import routes_bp

@routes_bp.route('/add_task', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        new_task = Task(task=task_content, complete=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('routes.home'))


@routes_bp.route('/toggle_task_complete/<int:task_id>')
def toggle_task_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('routes.project_tasks', project_id=task.project_id))


@routes_bp.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('routes.project_tasks', project_id=task.project_id))


@routes_bp.route('/project/<int:project_id>/add_task', methods=['POST'])
def add_project_task(project_id):
    project = Project.query.get_or_404(project_id)
    task_content = request.form.get('task')
    if task_content:
        new_task = Task(task=task_content, complete=False, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('routes.project_tasks', project_id=project_id))


@routes_bp.route('/project/<int:project_id>')
def project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('project_tasks.html', project=project, tasks=tasks)
