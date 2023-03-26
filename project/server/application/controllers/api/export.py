
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




@app.route("/api/posts/export_csv", methods=['GET'])
@auth_required('token')
def export_csv():
  post_dicts = [post.simplified_private_view(current_user) for post in current_user.posts]

  print(post_dicts)

  return jsonify(post_dicts, default=str)
