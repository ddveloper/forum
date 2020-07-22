import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, drop_db, User, Project, Category, Comment

DUMMY_PROJECTS_LEN_FOR_TEST = 15

class ForumTestCase(unittest.TestCase):
    ''' This class represents the forum-dz test case '''

    def setUp(self):
        ''' Define test variables and initialize app. '''
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, DUMMY_PROJECTS_LEN_FOR_TEST)

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
        self.comment_example = {
            'comments': "your project rocks",
            'user_id': 4,
            'project_id': 6
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        ''' Executed after each test '''
        drop_db()

    def test_add_project_pass(self):
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
        project.delete() # roll back

    def test_400_add_project_invalid_inputs(self):
        ''' Test adding a new project '''
        invalid_project = self.project_example
        del invalid_project['name'] # remove a request field
        res = self.client().post('/projects', json=invalid_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'invalid inputs of new project')

    def test_500_add_project_server_error(self):
        ''' Test adding a new project '''
        drop_db() # delete table ahead of request
        res = self.client().post('/projects', 
                        json=self.project_example)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'failed to add new project')

    def test_get_projects_pass(self):
        ''' Test get projects '''
        res = self.client().get('/projects')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['length'], DUMMY_PROJECTS_LEN_FOR_TEST)
        self.assertEqual(len(data['projects']), DUMMY_PROJECTS_LEN_FOR_TEST)
        for i in range(DUMMY_PROJECTS_LEN_FOR_TEST):
            self.assertEqual(data['projects'][i]['name'], 
                            'dummy project{}'.format(i+1))

    def test_500_get_projects_server_error(self):
        ''' Test get projects '''
        drop_db() # delete table ahead of request
        res = self.client().get('/projects')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'failed to query projects')

    def test_add_comment_pass(self):
        ''' Test adding a new comment '''
        # check db status before request
        comment = Comment.query.filter_by(
            comments=self.comment_example['comments']).one_or_none()
        self.assertIsNone(comment)
        # activate the request
        res = self.client().post('/comments', 
                        json=self.comment_example)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        comment = Comment.query.filter_by(
            comments=self.comment_example['comments']).one_or_none()
        self.assertIsNotNone(comment)
        comment.delete() # roll back

    def test_400_add_comment_invalid_inputs(self):
        ''' Test adding a new comment '''
        invalid_comment = self.comment_example
        del invalid_comment['project_id'] # remove a request field
        res = self.client().post('/comments', json=invalid_comment)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'invalid inputs of new comment')

    def test_500_add_comment_server_error(self):
        ''' Test adding a new comment '''
        drop_db() # delete table ahead of request
        res = self.client().post('/comments', 
                        json=self.comment_example)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'failed to add new comment')

    def test_get_comments_pass(self):
        ''' Test get comments related to one project'''
        project_id = 10
        res = self.client().get('/comments/{}'.format(project_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['length'], 1)
        self.assertEqual(len(data['comments']), 1)
        self.assertEqual(data['comments'][0]['project_id'], project_id)

    def test_500_get_comments_server_error(self):
        ''' Test get comments '''
        drop_db() # delete table ahead of request
        project_id = 10
        res = self.client().get('/comments/{}'.format(project_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['messages'], 'failed to query comments')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()