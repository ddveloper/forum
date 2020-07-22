import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, drop_db, User, Project, Category, Comment

class ForumTestCase(unittest.TestCase):
    ''' This class represents the forum-dz test case '''

    def setUp(self):
        ''' Define test variables and initialize app. '''
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, True)

        # a project metadata for tests
        self.project_example = {
            'name': "test project",
            'description': "I am a project for running tests",
            'category': 2,
            'labels': "nodejs, react, auth0",
            'image_link': "https://test_image_link",
            'video_link': "https://test_video_link",
        }
        # a comment metadata for tests

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        ''' Executed after each test '''
        drop_db()

    def test_create_project(self):
        ''' Test adding a new project '''
        # check db status before request
        project = Project.query.filter_by(
            name=self.project_example['name']).one_or_none()
        self.assertIsNone(project)
        # activate the request
        res = self.client().post('/projects', 
                        json=self.project_example)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        project = Project.query.filter_by(
            name=self.project_example['name']).one_or_none()
        self.assertIsNotNone(project)
        project.delete()

    def test_400_create_project_invalid_inputs(self):
        ''' Test adding a new project '''
        invalid_project = self.project_example
        del invalid_project['name'] # remove a request field
        res = self.client().post('/projects', json=invalid_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'invalid inputs of new project')

    def test_500_create_project_server_error(self):
        ''' Test adding a new project '''
        drop_db() # delete table ahead of request
        res = self.client().post('/projects', 
                        json=self.project_example)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'failed to add new project')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()