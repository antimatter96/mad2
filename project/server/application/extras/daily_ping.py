import pdfkit
from jinja2 import Template
import datetime
from sqlalchemy import text
from sqlalchemy.orm import joinedload

from application.database.index import db
from application.database.models.user import User, UserLastSeen
from application.database.models.post import Post
from application.database.models.export_job import ExportJob

def users_to_ping():
  current_time = datetime.datetime.utcnow()
  one_day_ago = current_time - datetime.timedelta(days=1)

  potential_user_ids_ = UserLastSeen.query\
    .with_entities(UserLastSeen.user_id)\
    .filter(UserLastSeen.last_seen_at <= one_day_ago)\
    .all()

  potential_user_ids = set([id for (id, ) in potential_user_ids_])

  if len(potential_user_ids) == 0:
    return []

  potential_users = db.session.query(User)\
    .options(joinedload(User.following))\
    .filter(User.user_id.in_(list(potential_user_ids)))\
    .all()

  to_check = {}

  for potential_user in potential_users:
    to_check[potential_user.user_id] = set([following.user_id for following in potential_user.following])

  following_ids = set()
  for user_id in to_check:
    following_ids = following_ids.union(to_check[user_id])

  users_with_posts_in_last_day_ = db.session.query(Post)\
    .with_entities(Post.creator_id)\
    .filter(Post.creator_id.in_(list(following_ids)))\
    .filter(Post.hidden != True)\
    .filter(Post.created_at >= one_day_ago)\
    .all()

  users_with_posts_in_last_day = set([id for (id, ) in users_with_posts_in_last_day_])

  users_to_ping_ids = []

  for user_id in to_check:
    if len(users_with_posts_in_last_day.intersection(to_check[user_id])) > 0:
      users_to_ping_ids.append(user_id)

  users_to_ping_ids = set(users_to_ping_ids)
  users_to_ping = []
  for potential_user in potential_users:
    if potential_user.user_id not in users_to_ping_ids:
      continue
    users_to_ping.append({ 'user_id': potential_user.user_id, 'email': potential_user.email, 'name': potential_user.name})

  return users_to_ping
