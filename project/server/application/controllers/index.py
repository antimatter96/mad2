import os

from flask import current_app as app
from flask import render_template, send_from_directory

from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
  return render_template('403.html'), 403

from flask import send_from_directory

from application.controllers.api.feed import *
from application.controllers.api.export import *
from application.controllers.api.user_graph import *


@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
