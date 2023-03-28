from flask import request, jsonify
from flask_security import current_user, auth_required

from application.database.index import db
from application.database.models.post import Post

from app import app as app

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

  return jsonify({ 'count': len(post_dicts), 'posts': post_dicts})
