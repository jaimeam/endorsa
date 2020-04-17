import os
from sqlalchemy import Table, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date

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
    
    return db


# Profile entity
class Profile(db.Model):
  __tablename__ = 'profile' # table name "user" is reserved in PostgreSQL

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
    try:
      db.session.add(self)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
  
  # Update model in database
  def update(self):
    try:
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

  # Delete model from database
  def delete(self):
    try:
      db.session.delete(self)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

  # Form representation of Profile model
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
    try:
      db.session.add(self)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
  
  # Update model in database
  def update(self):
    try:
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

  # Delete model from database
  def delete(self):
    try:
      db.session.delete(self)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

  # Form representation of Skill model
  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description
    }

# Endorsement entity
class Endorsement(db.Model):
  __tablename__ = 'endorsement'

  # Solution on handling multiple join paths/foreign keys here: 
  # https://docs.sqlalchemy.org/en/13/orm/join_conditions.html#handling-multiple-join-paths
  
  
  id = Column(Integer, primary_key=True)
  giver_id = Column(Integer, ForeignKey('profile.id', ondelete='CASCADE'), nullable=False)
  receiver_id = Column(Integer, ForeignKey('profile.id', ondelete='CASCADE'), nullable=False)
  skill_id = Column(Integer, ForeignKey('skill.id', ondelete='CASCADE'), nullable=False)
  creation_date = Column(DateTime, nullable=False)

  endorsement_giver = relationship("Profile", foreign_keys=[giver_id])
  endorsement_receiver = relationship("Profile", foreign_keys=[receiver_id])
  skill_endorsed = relationship("Skill")

  def __init__(self, giver_id, receiver_id, skill_id):
    self.giver_id = giver_id
    self.receiver_id = receiver_id
    self.skill_id = skill_id
    self.creation_date = date.today()

  # Insert new model in database
  def insert(self):
    try:
      db.session.add(self)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
  
  # Update model in database
  def update(self):
    try:
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

  # Delete model from database
  def delete(self):
    try:
      db.session.delete(self)
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()

  # Form representation of Endorsement model
  def format(self):
    return {
      'giver_id': self.giver_id,
      'receiver_id': self.receiver_id,
      'skill_id': self.skill_id,
      'creation_date': self.creation_date
    }