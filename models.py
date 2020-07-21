from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json, os, datetime

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, forTest=False):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    db.create_all()
    if forTest: add_dummy_data()

def drop_db():
    db.drop_all()

'''
add dummy data, for unittests
'''
def add_dummy_data():
  user1 = User(email_address="test@db.com", nick_name="tester")
  user1.insert()



'''
User
Have id, email_address, nick_name
'''
class User(db.Model):  
  __tablename__ = 'User'

  id = Column(Integer, primary_key=True)
  email_address = Column(String(120))
  nick_name = Column(String(120))
  projects = db.relationship('Project', backref='users', lazy=True)
  comments = db.relationship('Comment', backref='users', lazy=True)

  def __init__(self, email_address, nick_name):
    self.email_address = email_address
    self.nick_name = nick_name

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'email_address': self.email_address,
      'nick_name': self.nick_name}


'''
Project
Have name, description, category, labels, 
     favor_cnt, image_link, video_link,
     datetime and user_id (ForeignKey)
'''
class Project(db.Model):  
  __tablename__ = 'Project'

  id = Column(Integer, primary_key=True)
  name = Column(String(120))
  description = Column(String(500))
  category = Column(Integer)
  labels = Column(String(120))
  favor_cnt = Column(Integer, default=0)
  image_link = Column(String(500))
  video_link = Column(String(500))
  datetime = Column(DateTime, default=datetime.datetime.utcnow())
  user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
  comments = db.relationship('Comment', backref='projects', lazy=True)

  def __init__(self, name, description, category, 
                  labels, image_link, video_link,
                  user_id):
    self.name = name
    self.description = description
    self.category = category
    self.labels = labels
    self.image_link = image_link
    self.video_link = video_link
    self.user_id = user_id

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'category': self.category,
      'labels': self.labels,
      'image_link': self.image_link,
      'video_link': self.video_link,
      'datetime': self.datetime,
      'user_id': self.user_id}


'''
Comment
Have comments, datetime, 
    user_id and project_id as 2 foreign keys
'''
class Comment(db.Model):  
  __tablename__ = 'Comment'

  id = Column(Integer, primary_key=True)
  comments = Column(String(500))
  datetime = Column(DateTime)
  user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
  project_id = Column(Integer, ForeignKey('Project.id'), nullable=False)

  def __init__(self, comments, datetime, user_id, project_id):
    self.comments = comments
    self.datetime = datetime
    self.user_id = user_id
    self.project_id = project_id

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'comments': self.comments,
      'datetime': self.datetime,
      'user_id': self.user_id,
      'project_id': self.project_id}


'''
Category
Have id and name
'''
class Category(db.Model):  
  __tablename__ = 'Category'

  id = Column(Integer, primary_key=True)
  name = Column(String(120))

  def __init__(self, name):
    self.name = name

  def format(self):
    return {
      'id': self.id,
      'name': self.name}