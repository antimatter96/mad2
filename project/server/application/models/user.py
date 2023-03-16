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

  def public_view_as_dict(self):
    return {
        'post_id': getattr(self, 'post_id'),
        'title': getattr(self, 'title'),
        'content': getattr(self, 'content'),
        'creator': {
            'user_id': getattr(self.creator, 'user_id'),
            'email': getattr(self.creator, 'email')
        },
        'created_at': getattr(self, 'created_at'),
        'updated_at': getattr(self, 'updated_at'),
        'img_url': getattr(self, 'img_url'),
    }

  def public_view_wrt(self, current_user, with_posts=False):
    return {
        'user_id': getattr(self, 'user_id'),
        'email': getattr(self, 'email'),
        'follows_user': self in current_user.followers,
        'user_follows': self in current_user.following,
        #'posts': self.posts
    }
