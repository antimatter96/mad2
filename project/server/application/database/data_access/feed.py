from sqlalchemy import text

from cache import cache
from application.database.index import db
from application.database.models.user import User
from application.database.models.post import Post

@cache.memoize(timeout=120)
def _feed(user_id, from_int, limit_int):
  user = db.session.query(User)\
    .where(User.user_id == user_id)\
    .first()

  following_ids = [following.user_id for following in user.following]

  original_following_ids = len(following_ids)
  if len(following_ids) == 0:
    top_followed = db.session.execute(
        text(
            "SELECT following_user_id, COUNT(*) AS total_followers FROM follower_following GROUP BY following_user_id ORDER BY total_followers DESC LIMIT 5"
        )
    ).fetchall()
    following_ids = [following_user_id for (following_user_id, total_followers) in top_followed]

  posts = db.session.query(Post)\
    .filter(Post.creator_id.in_(following_ids))\
    .filter(Post.hidden != True)\
    .order_by(Post.updated_at)\
    .offset(from_int)\
    .limit(limit_int)\
    .all()

  post_dicts = [post.public_view_as_dict(user) for post in posts]

  return original_following_ids, post_dicts
