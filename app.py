from flask import Flask
from database_initialization import db
from project_routes import *
from task_routes import *
from routes import *

# Constants for configuration
DATABASE_URI = 'sqlite:///todo.db'
TRACK_MODIFICATIONS = False

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TRACK_MODIFICATIONS
db.init_app(app)  # Bind the database to the app

# Register routes
app.register_blueprint(routes_bp)  # Register routes from routes.py

with app.app_context():
    db.create_all()  # Create missing tables
    if not Project.query.first():  # Seed if empty
        db.session.add(Project(name="Example Project"))
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
