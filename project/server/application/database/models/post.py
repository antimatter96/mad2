from datetime import datetime
from sqlalchemy.orm import relationship

from application.database.index import db

class Post(db.Model):
  __tablename__ = 'post'
  post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  title = db.Column(db.String, nullable=False)
  content = db.Column(db.Text, nullable=False)

  img_url = db.Column(db.String, nullable=True)

  hidden = db.Column(db.Boolean())

  creator_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
  creator = relationship("User", back_populates="posts")

  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

  def public_view_as_dict(self, current_user):
    return {
        'post_id': getattr(self, 'post_id'),
        'title': getattr(self, 'title'),
        'content': getattr(self, 'content'),
        'creator': getattr(self, 'creator').public_view_wrt(current_user),
        'created_at': getattr(self, 'created_at'),
        'updated_at': getattr(self, 'updated_at'),
        'img_url': getattr(self, 'img_url'),
    }

  def private_as_dict(self, current_user):
    return {
        **self.public_view_as_dict(current_user),
        'hidden': getattr(self, 'hidden'),
    }

  def simplified_private_view(self, current_user):
    full_view = self.private_as_dict(current_user)
    del full_view['creator']
    return full_view

  def simplified_public_view(self, current_user):
    full_view = self.public_view_as_dict(current_user)
    del full_view['creator']
    return full_view
