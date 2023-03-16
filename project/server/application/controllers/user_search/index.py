import time
import bcrypt
import hashlib

from flask import current_app as app
from flask import request, jsonify
from flask import render_template, redirect, url_for, session

from application.models.user import User
from application.models.post import Post

from application.database.index import db

from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore

@app.route("/api/users/search_by_prefix", methods=['GET'])
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

@app.route("/api/feed/", methods=['GET'])
@auth_required('token')
def feed():
  content = request.get_json(force=True)
  from_int_s = content.get("from", "0").strip()
  limit_int_s = content.get("limit", "20").strip()

  try:
    from_int = int(from_int_s)
    limit_int = int(limit_int_s)
  except:
    from_int = 0
    limit_int = 0

  following_ids = [following.user_id for following in current_user.following]
  posts = db.session.query(Post)\
    .filter(Post.creator_id.in_(following_ids))\
    .filter(Post.hidden == True)\
    .order_by(Post.updated_at)\
    .offset(from_int)\
    .limit(limit_int)\
    .all()

  post_dicts = [post.public_view_as_dict() for post in posts]

  print(current_user)

  return jsonify({'count': len(post_dicts), 'posts': post_dicts})

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
