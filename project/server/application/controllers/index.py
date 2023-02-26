from flask import current_app as app
from flask import render_template

from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def not_authorized(e):
  return render_template('403.html'), 403

@app.route("/info", methods=['GET'])
@auth_required()
def render_signup():
  errors = []

  print(current_user)

  return "asd"

@app.route("/feed", methods=['GET'])
@auth_required()
def feed():
  errors = []

  print(current_user)

  return "asd"

@app.route("/search", methods=['GET'])
@auth_required()
def following():
  errors = []

  print(current_user)

  return "asd"
# from application.controllers.user.index import *
# from application.controllers.card.index import *
# from application.controllers.list.index import *
# from application.controllers.stats.index import *
