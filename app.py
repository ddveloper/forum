import os, sys
from flask import Flask, request, abort, jsonify, flash
from models import setup_db, User, Project, Category, Comment
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/project/add', methods=['POST'])
    def add_project():
        ''' Add a new project based on user inputs '''
        body = request.get_json()
        name = body.get('name', None)
        description = body.get('description', None)
        category = body.get('category', None)
        labels = body.get('labels', None)
        image_link = body.get('image_link', None)
        video_link = body.get('video_link', None)
        user_id = 1 # TODO get user_id from Auth info.
        
        if not name or not description or not category \
            or not labels or not image_link or not video_link:
            abort(400, 'invalid inputs of new project')
        print('adding ...')
        try:
            project = Project(name=name, description=description,
                            category=category, labels=labels, 
                            image_link=image_link, video_link=video_link,
                            user_id=user_id)
            project.insert()
            return jsonify({
                'success': True,
            })
        except:
            flash('An error occur when adding new project')
            print(sys.exc_info())
            abort(500, 'failed to add new project')

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"


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