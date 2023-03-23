
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




@app.route("/api/export_csv/", methods=['GET'])
@auth_required('token')
def export_csv():
  content = request.get_json(force=True)
  prefix = content["asd"].strip()

  following_ids = [following.user_id for following in current_user.following]
  posts = db.session.query(Post).filter(Post.creator_id.in_(following_ids)).filter(Post.hidden == True).order_by(Post.updated_at).all()

  post_dicts = [post.public_view_as_dict() for post in posts]

  print(current_user)

  return jsonify(post_dicts, default=str)

@app.route("/api/export_report/", methods=['GET'])
@auth_required('token')
def export_report():
  content = request.get_json(force=True)
  prefix = content["asd"].strip()

  following_ids = [following.user_id for following in current_user.following]
  posts = db.session.query(Post).filter(Post.creator_id.in_(following_ids)).filter(Post.hidden == True).order_by(Post.updated_at).all()

  post_dicts = [post.public_view_as_dict() for post in posts]

  print(current_user)

  return jsonify(post_dicts, default=str)
