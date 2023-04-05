from flask import request, jsonify
from flask_security import current_user, auth_required

from application.database.data_access.feed import _feed

from app import app as app

@app.route("/api/feed", methods=['GET'])
@auth_required('token')
def feed():
  content = request.args
  from_int_s = content.get("from", "0").strip()
  limit_int_s = content.get("limit", "40").strip()

  try:
    from_int = int(from_int_s)
  except:
    from_int = 0

  try:
    limit_int = int(limit_int_s)
    if limit_int > 40:
      limit_int = 40
  except:
    limit_int = 0

  following_count, post_dicts = _feed(current_user.user_id, from_int, limit_int)

  return jsonify({ 'count': len(post_dicts), 'posts': post_dicts, 'following_count': following_count})
