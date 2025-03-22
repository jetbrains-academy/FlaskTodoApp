import logging
from flask import request, redirect, url_for, render_template

from models import Project, Task
from database_initialization import db
from routes import routes_bp

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@routes_bp.route('/create_project', methods=['POST'])
def createProject():
    projectName = request.form.get('project_name')
    if projectName:
        try:
            logger.info(f"Attempting to create a new project with name: {projectName}")
            newProject = Project(name=projectName)
            db.session.add(newProject)
            db.session.commit()
            logger.info(f"Project '{projectName}' created successfully.")
        except Exception as e:
            logger.error(f"Error while creating project '{projectName}': {e}")
    else:
        logger.warning("Project name not provided in the request.")
    return redirect(url_for('routes.home'))


@routes_bp.route('/delete_project/<int:project_id>', methods=['POST'])
def deleteProject(projectId):
    try:
        logger.info(f"Fetching project with ID: {projectId} for deletion.")
        project = Project.query.get_or_404(projectId)
        logger.info(f"Project found: {project.name}. Deleting associated tasks.")
        Task.query.filter_by(project_id=projectId).delete()  # Cascade delete tasks
        db.session.delete(project)
        db.session.commit()
        logger.info(f"Project with ID {projectId} deleted successfully.")
    except Exception as e:
        logger.error(f"Error while deleting project with ID {projectId}: {e}")
    return redirect(url_for('routes.home'))
