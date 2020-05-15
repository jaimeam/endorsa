import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Profile, Skill, Endorsement
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
auth_header_admin = {'Authorization': 'bearer '+config['TOKEN']['admin']}
auth_header_user = {'Authorization': 'bearer '+config['TOKEN']['user']}

class EndorsaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # -----------------ADMIN RIGHTS----------------------------

    # ----USERS----

    # Delete all users
    def test_delete_users_admin(self):
        res = self.client().delete('/users', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
    
    # Error 404 as no users are found
    def test_get_users_admin_404(self):
        res = self.client().get('/users', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Post user
    def test_post_user_admin(self):
        res = self.client().post('/users', headers = auth_header_admin,
        json = 
        {
            "first_name": "Vincent",
            "last_name": "Vega",
            "location": "California",
            "description": "Freelance Gangster | MBA",
            "contact": "123456789"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['user']['first_name'], 'Vincent')

    # Error 404 due to missing last_name field
    def test_post_user_admin_422(self):
        res = self.client().post('/users', headers = auth_header_admin,
        json = 
        {
            "first_name": "Vincent",
            "location": "California",
            "description": "Freelance Gangster | MBA",
            "contact": "123456789"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
    
    # Error 404 as no user 1000 is found
    def test_get_user_1000_admin(self):
        res = self.client().get('/users/1000', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # ----SKILLS----

    # Delete all skills
    def test_delete_skills_admin(self):
        res = self.client().delete('/skills', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
    
    # Error 404 as no skills are found
    def test_get_skills_admin_404(self):
        res = self.client().get('/skills', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Post skill
    def test_post_skill_admin(self):
        res = self.client().post('/skills', headers = auth_header_admin,
        json = 
        {
            "name": "Problem solving",
            "description": "Ability to deal with complex situations and come up with a solution"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['skill']['name'], 'Problem solving')

    # Error 404 due to missing name field
    def test_post_skill_admin_422(self):
        res = self.client().post('/skills', headers = auth_header_admin,
        json = 
        {
            "description": "Ability to deal with complex situations and come up with a solution"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
    
    # Error 404 as no skill 1000 is found
    def test_get_skill_1000_admin_404(self):
        res = self.client().get('/skills/1000', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # ----ENDORSEMENTS----

    # Delete all endorsements
    def test_delete_endorsements_admin(self):
        res = self.client().delete('/endorsements', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
    
    # Error 404 as no endorsements are found
    def test_get_endorsements_admin_404(self):
        res = self.client().get('/endorsements', headers = auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Error 404 due to non-existing users and skills
    def test_post_endorsement_admin_422(self):
        res = self.client().post('/endorsements', headers = auth_header_admin,
        json = 
        {
            "giver_id": "1000",
            "receiver_id": "2000",
            "skill_id": "1000"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    # -----------------USER RIGHTS----------------------------

    # ----USERS----

    # Error 401 due to no authorization to edit
    def test_delete_users_user_401(self):
        res = self.client().delete('/users', headers = auth_header_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    # Error 404 as no users are found
    def test_get_users_user_404(self):
        res = self.client().get('/users', headers = auth_header_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Error 401 due to no authorization to edit
    def test_post_user_user_401(self):
        res = self.client().post('/users', headers = auth_header_user,
        json = 
        {
            "first_name": "Vincent",
            "last_name": "Vega",
            "location": "California",
            "description": "Freelance Gangster | MBA",
            "contact": "123456789"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # ----SKILLS----

    # Error 401 due to no authorization to edit
    def test_delete_skills_user_401(self):
        res = self.client().delete('/skills', headers = auth_header_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Error 404 as no skills are found
    def test_get_skills_user_404(self):
        res = self.client().get('/skills', headers = auth_header_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Error 401 due to no authorization to edit
    def test_post_skill_user_401(self):
        res = self.client().post('/skills', headers = auth_header_user,
        json = 
        {
            "name": "Problem solving",
            "description": "Ability to deal with complex situations and come up with a solution"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


    # ----ENDORSEMENTS----

    # Error 401 due to no authorization to edit
    def test_delete_endorsements_user_401(self):
        res = self.client().delete('/endorsements', headers = auth_header_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    # Error 404 as no endorsements are found
    def test_get_endorsements_user_404(self):
        res = self.client().get('/endorsements', headers = auth_header_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # Error 401 due to no authorization to edit
    def test_post_endorsement_user_401(self):
        res = self.client().post('/endorsements', headers = auth_header_user,
        json = 
        {
            "giver_id": "1000",
            "receiver_id": "2000",
            "skill_id": "1000"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()