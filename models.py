import os
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

# Bind a flask application and a SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    db.create_all()

# User entity
class User(db.Model):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  location = Column(String)
  description = Column(String)
  contact = Column(Integer)

  def __init__(self, first_name, last_name, location, description, contact):
    self.first_name = first_name
    self.last_name = last_name
    self.location = location
    self.description = description
    self.contact = contact

  # Insert new model in database
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  # Update model in database
  def update(self):
    db.session.commit()

  # Delete model from database
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # Form representation of User model
  def format(self):
    return {
      'id': self.id,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'location': self.location,
      'description': self.description,
      'contact': self.contact
    }

# Skill entity
class Skill(db.Model):
  __tablename__ = 'skill'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  description = Column(String)

  def __init__(self, name, description):
    self.name = name
    self.description = description

  # Insert new model in database
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  # Update model in database
  def update(self):
    db.session.commit()

  # Delete model from database
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  # Form representation of Skill model
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
    }

# Endorsement entity
class Endorsement(db.Model):
  __tablename__ = 'endorsement'

  id = Column(Integer, primary_key=True)
  giver_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
  receiver_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
  skill_id = Column(Integer, ForeignKey('skill.id', ondelete='CASCADE'), nullable=False)
  creation_date = Column(DateTime, nullable=False)
  user = db.relationship(User,backref='endorsements')
  skill = db.relationship(Skill,backref='endorsements')