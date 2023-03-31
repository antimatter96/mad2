from datetime import datetime
from sqlalchemy.orm import relationship

from application.database.index import db

class ExportJob(db.Model):
  __tablename__ = 'export_job'

  job_id = db.Column(db.String, primary_key=True)

  done = db.Column(db.Boolean())
  error = db.Column(db.Boolean())
  deleted = db.Column(db.Boolean())

  file_path = db.Column(db.String)

  creator_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
  creator = relationship("User", back_populates="export_jobs")

  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

  def deadline_passed(self):
    time_passed = datetime.now() - self.created_at
    return time_passed.seconds > 60 * 60    # 1 hour

  def public_view(self):
    return {
        'job_id': getattr(self, 'job_id'),
        'created_at': getattr(self, 'created_at'),
        'done': getattr(self, 'done', False),
        'error': getattr(self, 'error', False),
        'expired': self.deadline_passed(),
        'deleted': getattr(self, 'deleted', False),
        **({ 'file_path': getattr(self, 'file_path')} if not self.deadline_passed() else {}),
    }
