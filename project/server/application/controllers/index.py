import os

from app import app as app
from flask import render_template, send_from_directory
from flask_sse import sse
from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
  return render_template('403.html'), 403

from flask import send_from_directory

from application.controllers.feed import *
from application.controllers.export import *
from application.controllers.user_graph import *

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@sse.before_request
@auth_required('token', 'session')
def check_access():
  if request.args.get("channel") == None:
    return redirect(url_for('sse.stream', channel="users." + str(current_user.user_id)))

  channel = request.args.get("channel", "users.-1", type=str)
  try:
    requested_user_id = int(channel.split(".")[1])
  except:
    return '', 403

  if current_user.user_id != requested_user_id:
    return '', 403

@sse.after_request
def add_header(response):
  response.headers['Access-Control-Allow-Credentials'] = 'true'
  return response
