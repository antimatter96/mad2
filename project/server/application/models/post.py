from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

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

  @hybrid_property
  def deadline_passed(self):
    if self.complete:
      return self.completed_on > self.deadline
    return datetime.now() > self.deadline
