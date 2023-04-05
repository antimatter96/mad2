import datetime
from sqlalchemy import text

from application.database.index import db
from application.database.models.user import User
from application.database.models.post import Post
from application.database.models.export_job import ExportJob
from application.database.data_access.utils import new_entities

def _monthly_data():
  current_time = datetime.datetime.utcnow()
  thirty_days_ago = current_time - datetime.timedelta(days=30)
  sixty_days_ago = current_time - datetime.timedelta(days=60)

  users_this_month = new_entities(User, thirty_days_ago, current_time)
  users_last_month = new_entities(User, sixty_days_ago, thirty_days_ago)

  posts_this_month = new_entities(Post, thirty_days_ago, current_time)
  posts_last_month = new_entities(Post, sixty_days_ago, thirty_days_ago)

  exports_this_month = new_entities(ExportJob, thirty_days_ago, current_time)
  exports_last_month = new_entities(ExportJob, sixty_days_ago, thirty_days_ago)

  followers_count_result = db.session.execute(
      text("SELECT COUNT(*) FROM follower_following WHERE created_at >= :from_date AND created_at < :to_date"
          ).bindparams(to_date=current_time, from_date=thirty_days_ago)
  )
  for r in followers_count_result:
    followers_count = r[0]

  max_creator_result = db.session.execute(
      text(
          "SELECT creator_id, COUNT(*) AS create_count FROM post WHERE created_at >= :from_date AND created_at < :to_date GROUP BY creator_id ORDER BY create_count DESC limit 1"
      ).bindparams(to_date=current_time, from_date=thirty_days_ago)
  )
  for r in max_creator_result:
    (max_creator_id, max_creator_count) = r

  max_creator = db.session.query(User)\
    .where(User.user_id == max_creator_id)\
    .first()

  return {
      'stats': {
          'users': {
              'delta': users_this_month - users_last_month,
              'percentage': 100 * 1 if users_last_month == 0 else ((users_this_month / users_last_month) - 1),
          },
          'posts': {
              'delta': posts_this_month - posts_last_month,
              'percentage': 100 * 1 if posts_last_month == 0 else ((posts_this_month / posts_last_month) - 1),
          },
          'exports': {
              'delta': exports_this_month - exports_last_month,
              'percentage': 100 * 1 if exports_last_month == 0 else ((exports_this_month / exports_last_month) - 1),
          },
          'followers_count': followers_count,
          'max_creator_obj': max_creator,
          'max_creator_count': max_creator_count,
      },
      'from': thirty_days_ago.strftime("%Y-%m-%d"),
      'to': current_time.strftime("%Y-%m-%d"),
  }
