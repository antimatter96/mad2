from flask import current_app as app
from flask import render_template

from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore

from application.models.post import Post

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
  return render_template('403.html'), 403


from application.controllers.user_search.index import *
