from datetime import datetime
import os
import csv

from flask_sse import sse
from flask import current_app as app
from werkzeug.utils import secure_filename

from application.background_workers.index import celery
from application.database.index import db
from application.models.user import User
from application.models.export_job import ExportJob

EXPORT_CSV_KEYS = ['post_id', 'created_at', 'title', 'content', 'updated_at', 'hidden']

@celery.task()
def export_csv(user_id):
  print("started export_csv for", user_id)
  job_id = export_csv.request.id

  export_job = ExportJob.query.filter(ExportJob.job_id == job_id).first()
  if export_job == None:
    print("job not found")
    return None

  user = User.query.filter(User.user_id == user_id).first()
  if user == None:
    print("user not found")
    return None

  post_dicts = [post.simplified_private_view(user) for post in user.posts]
  for post in post_dicts:
    post['content'] = post['content'].replace('\n', " ⏎ ")
    post['title'] = post['title'].replace('\n', " ⏎ ")

  filename = secure_filename(str(user_id) + "_" + job_id + ".csv")
  file_saved = False
  try:
    with open(os.path.join(app.config['CSV_UPLOAD_FOLDER'], filename), "w") as f:
      dict_writer = csv.DictWriter(f, EXPORT_CSV_KEYS, extrasaction='ignore', delimiter=',')
      dict_writer.writeheader()
      dict_writer.writerows(post_dicts)
    file_saved = True
  except Exception as e:
    print(e)

  try:
    if file_saved:
      export_job.done = True
      export_job.file_path = filename
    else:
      export_job.done = False
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
    raise e

  sse.publish({ "message": "done", "job_id": job_id}, type='jobDone', channel="users." + str(user_id))

  print("End export_csv", user_id)

@celery.task()
def delete_csv(job_id):
  print("started delete_csv for", job_id)

  export_job = ExportJob.query.filter(ExportJob.job_id == job_id).first()
  if export_job == None:
    return None

  try:
    if os.path.exists(os.path.join(app.config['CSV_UPLOAD_FOLDER'], export_job.file_path)):
      os.remove(os.path.join(app.config['CSV_UPLOAD_FOLDER'], export_job.file_path))
  except Exception as e:
    print(e)

  try:
    export_job.done = True
    export_job.file_path = None
    export_job.deleted = True
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
    raise e

  print("End delete_csv", job_id)
