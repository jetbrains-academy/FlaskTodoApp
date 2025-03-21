from flask import request, redirect, url_for, render_template

from models import Project, Task
from database_initialization import db
from routes import routes_bp


@routes_bp.route('/create_project', methods=['POST'])
def createProject():
    projectName = request.form.get('project_name')
    if projectName:
        newProject = Project(name=projectName)
        db.session.add(newProject)
        db.session.commit()
    return redirect(url_for('routes.home'))


@routes_bp.route('/delete_project/<int:project_id>', methods=['POST'])
def deleteProject(projectId):
    project = Project.query.get_or_404(projectId)
    Task.query.filter_by(project_id=projectId).delete()  # Cascade delete tasks
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('routes.home'))

@routes_bp.route('/project/<int:project_id>')
def projectTasks(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project_id).all()
    return render_template('project_tasks.html', project=project, tasks=tasks)
