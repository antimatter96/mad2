from cache import cache
from application.database.index import db
from application.database.models.user import User
from application.database.models.post import Post

@cache.memoize(timeout=6000)
def _private_view_with_followers(user_id):
  user = db.session.query(User)\
    .where(User.user_id == user_id)\
    .first()

  return user.private_view(with_followers_list=True)

@cache.memoize(timeout=6000)
def _private_view_with_following(user_id):
  user = db.session.query(User)\
    .where(User.user_id == user_id)\
    .first()

  return user.private_view(with_following_list=True)

@cache.memoize(timeout=6000)
def _self_view(user_id):
  user = db.session.query(User)\
    .where(User.user_id == user_id)\
    .first()
  return user.private_view(with_posts=True)

