import unittest
from database_initialization import db
from flask import Flask
from models import Task, Project
from task_routes import routes_bp
from project_routes import routes_bp


class TestAddProjectTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app.config['TESTING'] = True
        db.init_app(cls.app)
        cls.app.register_blueprint(routes_bp)  # Register the routes
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        with cls.app.app_context():
            db.create_all()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_add_task_to_nonexistent_project(self):
        response = self.client.post('/project/999/add_task', data={'task': 'Sample Task'})
        self.assertEqual(response.status_code, 404)

    def test_add_task_with_missing_task_field(self):
        with self.app.app_context():
            # Create and add the project
            project = Project(name='Test Project')
            db.session.add(project)
            db.session.commit()
            # Extract project ID before the session ends
            project_id = project.id

        # Use the project ID explicitly here
        response = self.client.post(f'/project/{project_id}/add_task', data={})
        self.assertEqual(response.status_code, 302)  # Redirection still occurs

        # Verify that no tasks were added
        with self.app.app_context():
            tasks = Task.query.filter_by(project_id=project_id).all()
            self.assertEqual(len(tasks), 0)  # Ensure no tasks were added

    def test_add_task_success(self):
        with self.app.app_context():
            project = Project(name='Test Project')
            db.session.add(project)
            db.session.commit()
            project_id = project.id

        response = self.client.post(f'/project/{project_id}/add_task', data={'task': 'Write Tests'})

        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            task = Task.query.filter_by(project_id=project_id, task='Write Tests').first()
            self.assertIsNotNone(task)
            self.assertEqual(task.task, 'Write Tests')
