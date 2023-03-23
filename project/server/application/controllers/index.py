import os

from app import cache
from flask import current_app as app
from flask import render_template, send_from_directory

from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore

from application.models.post import Post

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
  return render_template('403.html'), 403

from application.controllers.api.non_rest import *

from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
