from datetime import datetime
from sqlalchemy.orm import relationship
from flask_security import UserMixin, RoleMixin

from application.database.index import db
from cache import cache

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
    db.Column('following_user_id', db.Integer(), db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('created_at', db.DateTime(), default=datetime.now)
)

class UserLastSeen(db.Model):
  __tablename__ = 'users_last_seen'
  user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id'), primary_key=True)
  last_seen_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
  rand_number = db.Column(db.Integer())

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  email = db.Column(db.String, unique=True, index=True)
  name = db.Column(db.String)
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
  export_jobs = relationship("ExportJob", back_populates="creator")

  def public_view_as_dict(self, current_user, with_posts=False):
    return {
        'user_id': getattr(self, 'user_id'),
        'email': getattr(
            self,
            'email',
        ),
        'name': getattr(self, 'name', None),
        'created_at': getattr(self, 'created_at'),
        'followers': { 'length': len(self.followers)},
        'following': { 'length': len(self.following)},
         **({
            'posts': sorted([post.simplified_public_view(current_user) for post in self.posts if post.hidden == False], key=lambda x: x['created_at'], reverse=True)
        } if with_posts else {}),
    }

  def public_view_wrt(self, current_user, with_posts=False):
    return {
        **self.public_view_as_dict(current_user, with_posts=with_posts),
        'follows_user': self in current_user.followers,
        'user_follows': self in current_user.following,
        'is_actually_user': self.user_id == current_user.user_id,
    }

  def private_view(self, with_posts=False, with_followers_list=False, with_following_list=False):
    return {
        **self.public_view_as_dict(self, with_posts=with_posts),
        **({
            'posts': sorted([post.simplified_private_view(self) for post in self.posts], key=lambda x: x['created_at'], reverse=True)
        } if with_posts else {}),
        **({
            'following': {
                'length': len(self.following),
                'list': [user_follows.public_view_wrt(self) for user_follows in self.following],
            },
        } if with_followers_list else {}),
        **({
            'followers': {
                'length': len(self.followers),
                'list': [user_following.public_view_wrt(self) for user_following in self.followers],
            },
        } if with_following_list else {}),
        'is_actually_user':
            True,
    }
