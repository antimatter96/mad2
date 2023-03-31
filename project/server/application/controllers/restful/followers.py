from flask_restful import current_app as app
from flask_restful import Resource
from flask_security import auth_required, current_user

from cache import cache

from application.database.models.user import User
from application.database.data_access import _private_view_with_followers, _private_view_with_following, _self_view, _feed

from application.database.index import db
from application.controllers.restful.errors import NotFoundError, BusinessValidationError, InternalServerError, common_errors

follower_api_errors = { "user_001": "User does not exist", "user_002": "User can't follow itself"}

class FollowersAPI(Resource):
  method_decorators = [auth_required("token")]

  def delete(self, other_user_id):
    print("unfollow", current_user.user_id, other_user_id)

    other_user = db.session.query(User)\
      .filter(User.user_id == other_user_id)\
      .first()

    if other_user is None:
      return '', 200

    try:
      if other_user in current_user.following:
        current_user.following.remove(other_user)
        db.session.commit()
        _clear_graph_cache(current_user.user_id, other_user_id)
      else:
        return '', 304
    except Exception as e:
      db.session.rollback()
      app.log_exception(e)
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return '', 200

  def post(self, other_user_id):
    print("follow", current_user.user_id, other_user_id)

    if current_user.user_id == other_user_id:
      raise BusinessValidationError(status_code=400, error_code='user_002', error_message=follower_api_errors['user_002'])

    other_user = db.session.query(User)\
      .filter(User.user_id == other_user_id)\
      .first()

    if other_user is None:
      raise NotFoundError(error_code='user_001', error_message=follower_api_errors['user_001'])

    try:
      if other_user not in current_user.following:
        current_user.following.append(other_user)
        db.session.commit()
        _clear_graph_cache(current_user.user_id, other_user_id)
      else:
        return '', 304
    except Exception as e:
      db.session.rollback()
      app.log_exception(e)
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return '', 200

def _clear_graph_cache(user_id_1, user_id_2):
  cache.delete_memoized(_private_view_with_followers, user_id_1)
  cache.delete_memoized(_private_view_with_followers, user_id_2)
  cache.delete_memoized(_private_view_with_following, user_id_1)
  cache.delete_memoized(_private_view_with_following, user_id_2)
  cache.delete_memoized(_self_view, user_id_1)
  cache.delete_memoized(_self_view, user_id_2)
  cache.delete_memoized(_feed, user_id_1, 0, 40)
