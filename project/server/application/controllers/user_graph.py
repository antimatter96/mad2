from flask import request, jsonify
from flask_security import current_user, auth_required

from cache import cache
from app import app as app

from application.models.user import User, _private_view_with_followers
from application.database.index import db

@app.route("/api/users/search_by_prefix", methods=['GET'])
##@cache.cached(timeout=5000)
@auth_required('token')
def user_search_by_prefix():
  content = request.args
  prefix = content.get("prefix", "").strip()

  if prefix != "":
    user_ids = _creator_ids_by_prefix(prefix)
    try:
      users = User.query\
        .filter(User.user_id.in_(user_ids))\
        .all()

      res = []

      for u in users:
        if u.user_id == current_user.user_id:
          continue
        res.append(u.public_view_wrt(current_user))

      return jsonify({ 'count': len(res), 'users': res})
    except:
      return {}
  else:
    return {}, 400

@cache.memoize(60)
def _creator_ids_by_prefix(prefix):
  search = "{}%".format(prefix)
  users = User.query\
    .filter(User.email.like(search))\
    .with_entities(User.user_id)\
    .limit(21)\
    .all()
  user_ids = [user_id for (user_id, ) in users]
  return user_ids

@app.route("/api/users/me", methods=['GET'])
##@cache.cached(timeout=5000)
@auth_required('token')
def my_profile():
  return jsonify(current_user.private_view(with_posts=True))

@app.route("/api/users/my_follows", methods=['GET'])
@auth_required('token')
def my_followers():
  return jsonify(_private_view_with_followers(current_user.user_id))

@app.route("/api/users/follow_me", methods=['GET'])
@auth_required('token')
def my_following():
  return jsonify(_private_view_with_followers(current_user.user_id))

@app.route("/api/users/<int:user_id>", methods=['GET'])
@auth_required('token')
def get_user_by_id(user_id):
  other_user = db.session\
    .query(User)\
    .filter(User.user_id == user_id)\
    .first()

  if other_user == None:
    return {}, 404

  if other_user.user_id == current_user.user_id:
    return jsonify(current_user.private_view(with_posts=True))

  return jsonify(other_user.public_view_wrt(current_user, with_posts=True))
