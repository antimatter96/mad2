import time
import bcrypt
import hashlib

from app import cache
from flask import current_app as app
from flask import request, jsonify
from flask import render_template, redirect, url_for, session

from application.models.user import User
from application.models.post import Post

from application.database.index import db

from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore


@app.route("/api/users/search_by_prefix", methods=['GET'])
##@cache.cached(timeout=5000)
@auth_required('token')
def user_search_by_prefix():
  content = request.get_json(force=True)
  prefix = content.get("prefix", "").strip()

  if prefix != "":
    search = "{}%".format(prefix)
    try:
      users = User.query\
        .filter(User.email.like(search))\
        .limit(20)\
        .all()

      res = []

      for u in users:
        if u.user_id == current_user.user_id:
          continue
        res.append(u.public_view_wrt(current_user, with_posts=True))

      return jsonify(res)
    except:
      return None
  else:
    return {}, 400

@app.route("/followers", methods=['GET'])
def render_signup():
  ...

@app.route("/following", methods=['GET'])
def render_signin():
  ...
