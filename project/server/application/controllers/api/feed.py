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


@app.route("/api/feed", methods=['GET'])
@auth_required('token')
def feed():
  content = request.args
  from_int_s = content.get("from", "0").strip()
  limit_int_s = content.get("limit", "40").strip()

  try:
    from_int = int(from_int_s)
    limit_int = int(limit_int_s)
    if limit_int > 40:
      limit_int = 40
  except:
    from_int = 0
    limit_int = 0

  following_ids = [following.user_id for following in current_user.following]
  posts = db.session.query(Post)\
    .filter(Post.creator_id.in_(following_ids))\
    .filter(Post.hidden != True)\
    .order_by(Post.updated_at)\
    .offset(from_int)\
    .limit(limit_int)\
    .all()

  post_dicts = [post.public_view_as_dict(current_user) for post in posts]

  return jsonify({'count': len(post_dicts), 'posts': post_dicts})
