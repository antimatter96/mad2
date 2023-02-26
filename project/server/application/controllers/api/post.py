from datetime import datetime

import werkzeug
from flask_restful import current_app as app
from flask_restful import Resource, fields, marshal_with, reqparse, inputs

from application.models.post import Post
from application.models.list import List

from application.database.index import db
from application.controllers.api.utils import token_required, min_length
from application.controllers.api.errors import NotFoundError, BusinessValidationError, InternalServerError, common_errors

class SimpleDateTime(fields.Raw):

  def format(self, value):
    return value.strftime('%Y-%m-%d')

post_errors = {
    "post_001": "List does not exist",
    "post_009": "Post does not exist",
}

post_fields = {
    "post_id": fields.Integer,
    "creator_id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "hidden": fields.Boolean,
    "image_url": fields.String,
    "created_at": SimpleDateTime,
    "updated_at": SimpleDateTime,
}

post_update_parser = reqparse.RequestParser()
post_update_parser.add_argument('title', type=min_length(1), required=True, trim=True)
post_update_parser.add_argument('content', type=min_length(1), required=True, trim=True)
post_update_parser.add_argument('hidden', type=inputs.boolean, default=False)
post_update_parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

post_create_parser = post_update_parser.copy()

class PostsAPI(Resource):
  method_decorators = [token_required]

  @marshal_with(post_fields)
  def get(self, current_user, post_id):
    post = db.session.query(Post).filter(Post.post_id == post_id).first()
    if post is None:
      raise NotFoundError(error_code='post_009', error_message=post_errors['post_009'])

    return post, 200

  def delete(self, current_user, post_id):
    post = db.session.query(Post).filter(Post.post_id == post_id and Post.creator_id == current_user.user_id).first()
    if post is None:
      raise NotFoundError(error_code='post_009', error_message=post_errors['post_009'])

    try:
      db.session.delete(post)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      app.log_exception(e)
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return '', 200

  @marshal_with(post_fields)
  def put(self, current_user, post_id):
    post = db.session.query(Post).filter(Post.post_id == post_id and Post.creator_id == current_user.user_id).first()
    if post is None:
      raise NotFoundError(error_code='post_009', error_message=post_errors['post_009'])

    args = post_update_parser.parse_args()

    title = args.get('title')
    content = args.get('content')
    hidden = args.get('hidden', False)
    image_url = args.get('image', None)

    try:
      post.title = title
      post.content = content
      post.hidden = hidden
      post.image_url = image_url
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return post

  @marshal_with(post_fields)
  def post(self, current_user):
    args = post_create_parser.parse_args()

    title = args.get('title')
    content = args.get('content')
    hidden = args.get('hidden', False)
    image_url = args.get('image', None)


    try:
      new_post = Post(title=title, content=content, hidden=hidden, creator=current_user, image_url=image_url)
      db.session.add(new_post)
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return new_post
