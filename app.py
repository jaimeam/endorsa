# Import libraries
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import aliased
from models import setup_db, Profile, Skill, Endorsement
from auth import AuthError, requires_auth
from jose import jwt

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
    @requires_auth('read:user')
    def get_users(jwt):
        users = [user.format() for user in Profile.query.all()]

        if (len(users) == 0):
            abort(404)

        return jsonify({
        'success':True,
        'users':users,
        'num_users':len(users)
        })
    
    # Delete all users
    @app.route('/users', methods=['DELETE'])
    @requires_auth('edit:user')
    def delete_all_users(jwt):
        # Delete all rows from model Profile
        num_deleted_rows = db.session.query(Profile).delete()
        db.session.commit()

        if (len(Profile.query.all()) != 0):
            abort(422)

        return jsonify({
        'success':True,
        'num_users_deleted':num_deleted_rows
        })
    
    # Create a new user via POST
    @app.route('/users', methods=['POST'])
    @requires_auth('edit:user')
    def post_new_user(jwt):
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

            # Create new entry in database
            new_user.insert()

            return jsonify({
                'success':True,
                'user': new_user.format()
            })
        except:
            db.session.rollback()
            abort(422)
    
    # Get detailed info of a selected user, including info on endorsements
    @app.route('/users/<id>', methods=['GET'])
    @requires_auth('read:user')
    def user_profile(jwt,id):
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
    
    # Modify a selected user via PATCH
    @app.route('/users/<id>', methods=['PATCH'])
    @requires_auth('edit:user')
    def patch_user(jwt,id):
        try:
            user = Profile.query.filter(Profile.id == id).one_or_none()
            # Raise error if no user is found with this ID
            if user == None:
                abort(404)

            # Get request data
            req_data = request.get_json()
            new_first_name = req_data.get('first_name', None)
            new_last_name = req_data.get('last_name', None)
            new_location = req_data.get('location', None)
            new_description = req_data.get('description', None)
            new_contact = req_data.get('contact', None)

            # Modify new values
            if new_first_name:
                user.first_name = new_first_name
            if new_last_name:
                user.last_name = new_last_name
            if new_location:
                user.location = new_location
            if new_description:
                user.description = new_description
            if new_contact:
                user.contact = new_contact

            user.update()

            return jsonify({
                'success':True,
                'user': user.format()
            })
        except:
            db.session.rollback()
            abort(422)

    
    # Delete a selected user
    @app.route('/users/<id>', methods=['DELETE'])
    @requires_auth('edit:user')
    def delete_user(jwt,id):
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
            db.session.rollback()
            abort(422)
    
    # Get full list of skills
    @app.route('/skills', methods=['GET'])
    @requires_auth('read:skill')
    def get_skills(jwt):
        skills = [skill.format() for skill in Skill.query.all()]

        if (len(skills) == 0):
            abort(404)

        return jsonify({
        'success':True,
        'skills':skills,
        'num_skills':len(skills)
        })

    # Delete all skills
    @app.route('/skills', methods=['DELETE'])
    @requires_auth('edit:skill')
    def delete_all_skills(jwt):
        # Delete all rows from model Skill
        num_deleted_rows = db.session.query(Skill).delete()
        db.session.commit()

        if (len(Skill.query.all()) != 0):
            db.session.rollback()
            abort(422)

        return jsonify({
        'success':True,
        'num_skills_deleted':num_deleted_rows
        })

    # Create a new skill via POST
    @app.route('/skills', methods=['POST'])
    @requires_auth('edit:skill')
    def post_new_skill(jwt):
        try:
            # Get request data
            req_data = request.get_json()
            name = req_data.get('name')
            description = req_data.get('description', None)
            
            # Create new Skill instance
            new_skill = Skill(
                name = name,
                description = description
            )

            # Create new entry in database
            new_skill.insert()
            
            return jsonify({
                'success':True,
                'skill': new_skill.format()
            })
        except:
            db.session.rollback()
            abort(422)

    # Get detailed info of a selected Skill, including info on endorsements
    @app.route('/skills/<id>', methods=['GET'])
    @requires_auth('read:skill')
    def skill_profile(jwt,id):
        try:
            skill = Skill.query.filter(Skill.id == id).one_or_none()
            # Raise error if no user is found with this ID
            if skill == None:
                abort(404)

            # Create aliases to deal with ambiguous Profile for receivers and givers
            ProfileG = aliased(Profile)
            ProfileR = aliased(Profile)

            # Get detailed list if endorsements given for this skill, with users involved
            endorsements = Endorsement.query\
                .filter(Endorsement.skill_id == id)\
                .with_entities(Endorsement.giver_id, Endorsement.receiver_id, Endorsement.creation_date)\
                .join(ProfileG, Endorsement.giver_id==ProfileG.id)\
                .add_columns(ProfileG.first_name.label('giver_first_name'),ProfileG.last_name.label('giver_last_name'))\
                .join(ProfileR, Endorsement.receiver_id==ProfileR.id)\
                .add_columns(ProfileR.first_name.label('receiver_first_name'),ProfileR.last_name.label('receiver_last_name'))

            # Return all info
            return jsonify({
                'success':True,
                'skill': skill.format(),
                'endorsements': [e._asdict() for e in endorsements]
            })
        except:
            abort(404)

    # Modify a selected skill via PATCH
    @app.route('/skills/<id>', methods=['PATCH'])
    @requires_auth('edit:skill')
    def patch_skill(jwt,id):
        try:
            skill = Skill.query.filter(Skill.id == id).one_or_none()
            # Raise error if no skill is found with this ID
            if skill == None:
                abort(404)

            # Get request data
            req_data = request.get_json()
            new_name = req_data.get('name', None)
            new_description = req_data.get('description', None)

            # Modify new values
            if new_name:
                skill.name = new_name
            if new_description:
                skill.description = new_description

            skill.update()
            return jsonify({
                'success':True,
                'skill': skill.format()
            })
        except:
            db.session.rollback()
            abort(422)

    # Delete a selected skill
    @app.route('/skills/<id>', methods=['DELETE'])
    @requires_auth('edit:skill')
    def delete_skill(jwt,id):
        try:
            skill = Skill.query.filter(Skill.id == id).one_or_none()
            
            # Raise error if no skill is found with this ID
            if skill == None:
                abort(404)
            
            skill.delete()

            return jsonify({
                'success':True,
                'skill': skill.format()
            })
        except:
            db.session.rollback()
            abort(422)

    # Get full list of endorsements
    @app.route('/endorsements', methods=['GET'])
    @requires_auth('read:endorsement')
    def get_endorsements(jwt):
        try:
            endorsements = [endorsement.format() for endorsement in Endorsement.query.all()]

            if (len(endorsements) == 0):
                abort(404)

            # Create aliases to deal with ambiguous Profile for receivers and givers
            ProfileG = aliased(Profile)
            ProfileR = aliased(Profile)

            # Query full info of endorsements with users info
            endorsements = Endorsement.query\
                .with_entities(Endorsement.giver_id, Endorsement.receiver_id, Endorsement.creation_date)\
                .join(ProfileG, Endorsement.giver_id==ProfileG.id)\
                .add_columns(ProfileG.first_name.label('giver_first_name'),ProfileG.last_name.label('giver_last_name'))\
                .join(ProfileR, Endorsement.receiver_id==ProfileR.id)\
                .add_columns(ProfileR.first_name.label('receiver_first_name'),ProfileR.last_name.label('receiver_last_name'))\
                .join(Skill)\
                .add_columns(Skill.name)

            return jsonify({
            'success':True,
            'endorsements':[e._asdict() for e in endorsements],
            'num_endorsements':len([e._asdict() for e in endorsements])
            })
        except:
            abort(404)

    # Delete all endorsements
    @app.route('/endorsements', methods=['DELETE'])
    @requires_auth('edit:endorsement')
    def delete_all_endorsements(jwt):
        # Delete all rows from model Endorsement
        num_deleted_rows = db.session.query(Endorsement).delete()
        db.session.commit()

        if (len(Endorsement.query.all()) != 0):
            db.session.rollback()
            abort(422)

        return jsonify({
        'success':True,
        'num_endorsements_deleted':num_deleted_rows
        })

    # Create a new endorsement via POST
    @app.route('/endorsements', methods=['POST'])
    @requires_auth('edit:endorsement')
    def post_new_endorsement(jwt):
        try:
            # Get request data
            req_data = request.get_json()
            giver_id = req_data.get('giver_id')
            receiver_id = req_data.get('receiver_id')
            skill_id = req_data.get('skill_id')
            
            # Create new Endorsement instance
            new_endorsement = Endorsement(
                giver_id = giver_id,
                receiver_id = receiver_id,
                skill_id = skill_id
            )

            # Create new entry in database
            new_endorsement.insert()

            return jsonify({
                'success':True,
                'endorsement': new_endorsement.format()
            })
        except:
            db.session.rollback()
            abort(422)

    # Delete a selected endorsement
    @app.route('/endorsements/<id>', methods=['DELETE'])
    @requires_auth('edit:endorsement')
    def delete_endorsement(jwt):
        try:
            endorsement = Endorsement.query.filter(Endorsement.id == id).one_or_none()
            
            # Raise error if no endorsement is found with this ID
            if endorsement == None:
                abort(404)
            
            endorsement.delete()

            return jsonify({
                'success':True,
                'endorsement': endorsement.format()
            })
        except:
            db.session.rollback()
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

    @app.errorhandler(AuthError)
    def authorizationerror(error):
        return jsonify({
                        "success": False, 
                        "error": 401,
                        "message": "Authorization error"
        }), 401

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)