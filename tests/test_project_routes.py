import unittest
from database_initialization import db
from flask import Flask
from models import Project
from project_routes import routes_bp


class TestCreateProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config['TESTING'] = True
        db.init_app(cls.app)
        cls.app.register_blueprint(routes_bp)  # Register the routes
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.client = self.app.test_client()
        with self.app.app_context():
            db.session.begin()

    def tearDown(self):
        with self.app.app_context():
            db.session.rollback()

    def test_create_project_success(self):
        with self.app.app_context():
            response = self.client.post('/create_project', data={'project_name': 'Test Project'})
            project = Project.query.filter_by(name='Test Project').first()
            self.assertIsNotNone(project)
            self.assertEqual(project.name, 'Test Project')

    def test_create_project_missing_name(self):
        with self.app.app_context():
            response = self.client.post('/create_project', data={'project_name': ''})
            self.assertEqual(response.status_code, 302)  # Redirect to home
            projects = Project.query.all()
            self.assertEqual(len(projects), 0)

    def test_create_project_database_error(self):
        def mock_commit():
            raise Exception("Database error")

        with self.app.app_context():
            self.commit = db.session.commit
            db.session.commit = mock_commit
            response = self.client.post('/create_project', data={'project_name': 'Error Project'})
            self.assertEqual(response.status_code, 500)
            projects = Project.query.all()
            self.assertEqual(len(projects), 0)
            db.session.commit = self.commit


if __name__ == '__main__':
    unittest.main()
