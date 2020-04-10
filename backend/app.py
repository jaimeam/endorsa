# Import libraries
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, User, Skill, Endorsement

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # Use the after_request decorator to set Access-Control-Allow
  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,PUT,POST,DELETE,OPTIONS')
      return response

  @app.route('/', methods = ['GET'])
  def hello_heroku():
      return "Hello from Heroku!"

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(debug=True)