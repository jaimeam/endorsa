# Import libraries
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Profile, Skill, Endorsement

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)
    CORS(app)

    # Use the after_request decorator to set Access-Control-Allow
    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods = ['GET'])
    def welcome():
        return "Welcome to Endorsa!"

    # Get full list of users
    @app.route('/users', methods=['GET'])
    def get_users():
        users = [user.format() for user in Profile.query.all()]

        if (len(users) == 0):
            abort(404)

        return jsonify({
        'success':True,
        'users':users,
        'num_users':len(users)
        })
    
    # Create a new user via POST
    @app.route('/users', methods=['POST'])
    def post_new_user():
        try:
            # Get request data
            req_data = request.get_json()
            first_name = req_data.get('first_name')
            last_name = req_data.get('last_name')
            location = req_data.get('location', None)
            description = req_data.get('description', None)
            contact = req_data.get('contact', None)
            
            # Create new Profile instance
            new_user = Profile(
                first_name = first_name,
                last_name = last_name,
                location = location,
                description = description,
                contact = contact
            )
            new_user.insert()
            return jsonify({
                'success':True,
                'user': new_user.format()
            })
        except:
            abort(404)
    
    # Get detailed info of a selected user, including info on endorsements
    @app.route('/users/<id>', methods=['GET'])
    def user_profile(id):
        try:
            user = Profile.query.filter(Profile.id == id).one_or_none()
            # Raise error if no user is found with this ID
            if user == None:
                abort(404)

            # Get endorsements received, with giver's name and last name, and skill name
            endorsements_received = Endorsement.query\
                .filter(Endorsement.receiver_id == id)\
                .with_entities(Endorsement.giver_id, Endorsement.skill_id, Endorsement.creation_date)\
                .join(Profile, Endorsement.giver_id==Profile.id)\
                .add_columns(Profile.first_name,Profile.last_name)\
                .join(Skill)\
                .add_columns(Skill.name)

            # Get endorsements given
            endorsements_given = Endorsement.query\
                .filter(Endorsement.giver_id == id)\
                .with_entities(Endorsement.receiver_id, Endorsement.skill_id, Endorsement.creation_date)\
                .join(Profile, Endorsement.receiver_id==Profile.id)\
                .add_columns(Profile.first_name,Profile.last_name)\
                .join(Skill)\
                .add_columns(Skill.name)

            # Return all info
            return jsonify({
                'success':True,
                'user': user.format(),
                'endorsements_received': [e._asdict() for e in endorsements_received],
                'endorsements_given': [e._asdict() for e in endorsements_given]
            })
        except:
            abort(404)
    
    # Delete a selected user
    @app.route('/users/<id>', methods=['DELETE'])
    def user_info(id):
        try:
            user = Profile.query.filter(Profile.id == id).one_or_none()
            # Raise error if no user is found with this ID
            if user == None:
                abort(404)
            
            user.delete()

            return jsonify({
                'success':True,
                'user': user.format()
            })
        except:
            abort(422)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)