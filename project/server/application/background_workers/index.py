from celery import Celery

from flask import current_app as app

celery = Celery('C1')

class TaskWithContext(celery.Task):

  def __call__(self, *args, **kwds):
    with app.app_context():
      return self.run(*args, **kwds)
