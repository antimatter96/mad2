from datetime import datetime
from sqlalchemy.orm import relationship
from flask_security import UserMixin, RoleMixin

from application.database.index import db

class RolesUsers(db.Model):
  __tablename__ = 'roles_users'
  id = db.Column(db.Integer(), primary_key=True)
  user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id'))
  role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
  __tablename__ = 'role'
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

follower_following = db.Table(
    'follower_following', db.Column('follower_user_id', db.Integer(), db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('following_user_id', db.Integer(), db.ForeignKey('user.user_id'), primary_key=True)
)

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  email = db.Column(db.String, unique=True)
  name = db.Column(db.String, unique=False)
  password = db.Column(db.String(255))

  active = db.Column(db.Boolean())

  fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
  auth_token = db.Column(db.String(255))

  ## ==

  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

  ## ==

  following = db.relationship(
      'User',
      secondary=follower_following,
      primaryjoin=user_id == follower_following.c.following_user_id,
      secondaryjoin=user_id == follower_following.c.follower_user_id,
      backref='followers'
  )

  posts = relationship("Post", back_populates="creator")
