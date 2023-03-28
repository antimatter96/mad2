import os

from sqlalchemy import desc
from flask import jsonify, send_from_directory
from flask_security import current_user, auth_required

from app import app as app

from application.database.models.export_job import ExportJob
from application.database.index import db
import application.background_workers.tasks as tasks

@app.route("/api/post/export/", methods=['POST'])
@auth_required('token', 'session')
def export_csv():
  job = tasks.export_csv.apply_async((current_user.user_id, ), countdown=5)

  try:
    export_job = ExportJob(job_id=job.id, creator=current_user)
    db.session.add(export_job)
    db.session.commit()
  except Exception as e:
    app.log_exception(e)
    app.logger.error(e)
    db.session.rollback()

  return jsonify(export_job.public_view())

@app.route("/api/post/export/jobs", methods=['GET'])
@auth_required('token', 'session')
def list_jobs():
  export_jobs = ExportJob.query\
    .filter(ExportJob.creator_id == current_user.user_id)\
    .order_by(desc(ExportJob.created_at))\
    .all()

  res = []

  for j in export_jobs:
    res.append(j.public_view())

  return jsonify({ 'count': len(res), 'jobs': res})

@app.route("/api/post/export/<job_id>", methods=['GET'])
@auth_required('token', 'session')
def download_and_delete_export_csv(job_id):
  export_job = ExportJob.query\
    .filter(ExportJob.creator_id == current_user.user_id and ExportJob.job_id == job_id)\
    .order_by(desc(ExportJob.created_at))\
    .first()

  if export_job == None:
    return '', 404

  if not export_job.deadline_passed():
    tasks.delete_csv.apply_async((job_id, ), countdown=60 * 60)
    return send_from_directory(os.path.join(app.root_path, 'static', 'export_reports'), export_job.file_path)
  else:
    return '', 404
