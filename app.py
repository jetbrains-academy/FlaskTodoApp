from flask import Flask
from database_initialization import db
from routes import routes_bp  # Import blueprint for routes

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


if __name__ == '__main__':
    app.run(debug=True)
