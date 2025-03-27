import logging
from flask import request, redirect, url_for, render_template
from models import Project, Task
from database_initialization import db
from routes import routes_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define reusable constants
ERROR_CREATING_PROJECT = "An error occurred while creating the project"
ERROR_DELETING_PROJECT = "An error occurred while deleting the project"
ERROR_FETCHING_TASKS = "An error occurred while fetching tasks for the project"

TEMPLATE_PROJECT_DESCRIPTION = "project_description.html"
TEMPLATE_PROJECT_TASKS = "project_tasks.html"


# Reusable logging functions
def log_error(message, exception):
    logger.error("%s: %s", message, exception, exc_info=True)


def log_info(message, *args):
    logger.info(message, *args)


@routes_bp.route('/create_project', methods=['POST'])
def create_project():
    project_name = request.form.get('project_name')
    if not project_name:
        logger.warning("Project name is missing in the form data.")
        return redirect(url_for('routes.home'))

    try:
        log_info("Creating new project with name: %s", project_name)
        new_project = Project(name=project_name)
        db.session.add(new_project)
        db.session.commit()
        log_info("Project '%s' successfully created.", project_name)
    except Exception as e:
        log_error(ERROR_CREATING_PROJECT, e)
        return ERROR_CREATING_PROJECT, 500

    return redirect(url_for('routes.home'))


@routes_bp.route('/project/<int:project_id>/description')
def project_description(project_id):
    project_record = Project.query.get_or_404(project_id)
    return render_template(TEMPLATE_PROJECT_DESCRIPTION, project=project_record)


@routes_bp.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    try:
        log_info("Attempting to delete project with ID: %d", project_id)
        project_record = Project.query.get_or_404(project_id)
        Task.query.filter_by(project_id=project_id).delete()  # Cascade delete tasks
        db.session.delete(project_record)
        db.session.commit()
        log_info("Project with ID %d successfully deleted.", project_id)
    except Exception as e:
        log_error(ERROR_DELETING_PROJECT, e)
        return ERROR_DELETING_PROJECT, 500

    return redirect(url_for('routes.home'))


@routes_bp.route('/project/<int:project_id>')
def project_tasks(project_id):
    try:
        log_info("Fetching tasks for project with ID: %d", project_id)
        project_record = Project.query.get_or_404(project_id)
        tasks = Task.query.filter_by(project_id=project_id).all()
        log_info("Found %d tasks for project ID: %d", len(tasks), project_id)
    except Exception as e:
        log_error(ERROR_FETCHING_TASKS, e)
        return ERROR_FETCHING_TASKS, 500

    return render_template(TEMPLATE_PROJECT_TASKS, project=project_record, tasks=tasks)
