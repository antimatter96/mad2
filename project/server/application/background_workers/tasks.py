import os
import csv
import datetime

from flask import current_app as app
from flask_sse import sse
from werkzeug.utils import secure_filename
from celery.schedules import crontab
from jinja2 import Template

from application.background_workers.index import celery
from application.database.index import db
from application.database.models.user import User
from application.database.models.export_job import ExportJob
from application.database.data_access.daily_ping import users_to_ping as _users_to_ping
from application.database.data_access.monthly_data import _monthly_data
from application.extras.report_generator import create_pdf_report
from application.extras.emails import send_email

EXPORT_CSV_KEYS = ['post_id', 'created_at', 'title', 'content', 'updated_at', 'hidden']

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  # Executes every Monday morning at 7:30 a.m.
  sender.add_periodic_task(
      crontab(0, 0, day_of_month='1'),
      send_monthly_report,
  )

  sender.add_periodic_task(
      crontab(hour=19, minute=30),
      send_daily_ping,
  )

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
      export_job.error = True
    db.session.commit()
  except Exception as e:
    print(e)
    db.session.rollback()
    raise e

  sse.publish({ "message": "done", "job_id": job_id}, type='jobDone', channel="users." + str(user_id))

  print("End export_csv", user_id)
  return True

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
  return True

@celery.task()
def send_monthly_report():
  print("send_monthly_report", "start")
  try:
    stats = _monthly_data()
    template_path = os.path.join(app.root_path, 'application/templates', 'monthly_report.html')
    pdf_file_name = datetime.datetime.now().strftime("%Y_%m_%d") + ".pdf"
    pdf_file_path = os.path.join(app.root_path, 'static', 'export_reports', pdf_file_name)

    with open(template_path) as f:
      pdf_temp = Template(f.read())

    stats['keys'] = ['users', 'posts', 'exports']
    stats['stats']['max_creator'] = stats['stats']['max_creator_obj'].email
    content = pdf_temp.render(data=stats)

    with open(pdf_file_path + '.html', 'w') as f:
      f.write(content)

    create_pdf_report(content=content, out_file_location=pdf_file_path)

    subject = "Monthly Report from " + stats['from'] + " to " + stats['to']

    attachment = { 'filename': pdf_file_name, 'upload_path': pdf_file_path, 'subtype': 'pdf'}

    send_email(to='admin@arpit.com', plain_text=None, html_text=content, attachment=attachment, subject=subject)
  except Exception as e:
    print(e)
    raise e

  print("send_monthly_report", "end")
  return True

@celery.task()
def send_daily_ping():
  print("send_daily_ping", "start")

  try:
    template_path = os.path.join(app.root_path, 'application/templates', 'daily_reminder.html')
    with open(template_path) as f:
      html_temp = Template(f.read())

    subject = "Long time no see"

    users_to_ping = _users_to_ping()
    for user in users_to_ping:
      content = html_temp.render(user=user)
      send_email(to=user['email'], plain_text=content, html_text=content, attachment=None, subject=subject)

  except Exception as e:
    print(e)
    raise e

  print("send_daily_ping", "end")
  return True

@celery.task()
def delete_cover_image(full_file_path):

  try:
    if os.path.exists(full_file_path):
      os.remove(full_file_path)
  except Exception as e:
    print(e)
    raise e

  return True
