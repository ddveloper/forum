import os
import sys
from flask import (Flask, request, abort, jsonify, flash)
from models import (setup_db, User, Project, Category, Comment)
from flask_cors import CORS
from auth import (AuthError, requires_auth)


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app, 15)
    CORS(app)

    @app.route('/projects', methods=['GET'])
    def query_projects():
        ''' Query projects '''
        try:
            projects = Project.query.all()
            formatted_projects = [project.format() for project in projects]
            return jsonify({
                'success': True,
                'length': len(formatted_projects),
                'projects': formatted_projects
            })
        except Exception:
            flash('An error occur when querying all projects')
            # print(sys.exc_info())
            abort(500, 'failed to query projects')

    @app.route('/projects', methods=['POST', 'PATCH'])
    @requires_auth('update:projects')
    def add_project(payload):
        ''' Add/update a new/existing project based on user inputs '''
        to_create = request.method == 'POST'
        body = request.get_json()
        name = body.get('name', None)
        description = body.get('description', None)
        category = body.get('category', None)
        labels = body.get('labels', None)
        image_link = body.get('image_link', None)
        video_link = body.get('video_link', None)
        user_id = 1  # TODO get user_id from Auth info.

        if not name or not description or not category \
                or not labels or not image_link or not video_link:
            abort(400, 'invalid inputs of {} project'
                  .format('new' if to_create else 'update'))

        try:
            if to_create:
                project = Project(name=name, description=description,
                                  category=category, labels=labels,
                                  image_link=image_link, video_link=video_link,
                                  user_id=user_id)
                project.insert()
            else:  # to update
                project = Project.query.filter_by(name=name).one_or_none()
                project.description = description
                project.category = category
                project.labels = labels
                project.image_link = image_link
                project.video_link = video_link
                project.update()
            return jsonify({
                'success': True,
            })
        except Exception:
            flash('An error occur when adding {} project'
                  .format('new' if to_create else 'update'))
            # print(sys.exc_info())
            abort(500, 'failed to add {} project'
                  .format('new' if to_create else 'update'))

    @app.route('/projects/<int:project_id>', methods=['DELETE'])
    @requires_auth('delete:projects')
    def delete_projects(payload, project_id):
        ''' Delete project based on its id '''
        try:
            project = Project.query.filter_by(id=project_id).one_or_none()
            # delete projects' comments first to avoid key error
            comments = Comment.query.filter_by(project_id=project_id).all()
            for comment in comments:
                comment.delete()
            # delete project itself
            project.delete()

            return jsonify({
                'success': True
            })
        except Exception:
            flash('An error occur when deleting project {}'.format(project_id))
            # print(sys.exc_info())
            abort(500, 'failed to delete project')

    @app.route('/comments/<int:project_id>', methods=['GET'])
    def query_comments(project_id):
        ''' Query comments based on project ID'''
        try:
            project = Project.query.filter_by(id=project_id).one_or_none()
            if not project:
                abort(400, 'invalid inputs of project_id')
            comments = Comment.query.filter_by(id=project_id).all()
            formatted_comments = [comment.format() for comment in comments]
            return jsonify({
                'success': True,
                'length': len(formatted_comments),
                'comments': formatted_comments
            })
        except Exception:
            flash('An error occur when querying comments for project {}'
                  .format(project_id))
            # print(sys.exc_info())
            abort(500, 'failed to query comments')

    @app.route('/comments', methods=['POST'])
    @requires_auth('add:comments')
    def add_comment(payload):
        ''' Add a new comment based on user inputs '''
        body = request.get_json()
        comments = body.get('comments', None)
        project_id = body.get('project_id', None)
        user_id = 1  # TODO get user_id from Auth info.

        if not comments or not project_id or not user_id:
            abort(400, 'invalid inputs of new comment')

        try:
            comment = Comment(comments=comments,
                              project_id=project_id, user_id=user_id)
            comment.insert()
            return jsonify({
                'success': True,
            })
        except Exception:
            flash('An error occur when adding new comment')
            # print(sys.exc_info())
            abort(500, 'failed to add new comment')

    # error handling code below

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success': False,
            'messages': error.description
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'messages': error.description
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return jsonify({
            'success': False,
            'messages': error.description
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'messages': error.description
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
