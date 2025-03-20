from flask import Blueprint, render_template, request, redirect, url_for
from models import Project, Task
from database_initialization import db

# Create a blueprint for routes
routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def home():
    projects = Project.query.all()
    return render_template('base.html', projects=projects)

