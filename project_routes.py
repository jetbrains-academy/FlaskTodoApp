from flask import request, redirect, url_for, render_template

from models import Project, Task
from database_initialization import db
from routes import routes_bp


@routes_bp.route('/create_project', methods=['POST'])
def create_project():
    project_name = request.form.get('project_name')
    if project_name:
        new_project = Project(name=project_name)
        db.session.add(new_project)
        db.session.commit()
    return redirect(url_for('routes.home'))


@routes_bp.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    Task.query.filter_by(project_id=project_id).delete()  # Cascade delete tasks
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('routes.home'))

@routes_bp.route('/project/<int:project_id>')
def project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('project_tasks.html', project=project, tasks=tasks)
