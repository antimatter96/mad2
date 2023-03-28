from datetime import datetime
import os
import base64

from werkzeug.utils import secure_filename
from flask_restful import current_app as app
from flask_restful import Resource, fields, marshal_with, reqparse, inputs
from flask_security import auth_required, current_user

from application.database.models.post import Post
from application.database.index import db
from application.controllers.restful.utils import min_length
from application.controllers.restful.errors import NotFoundError, InternalServerError, common_errors

class SimpleDateTime(fields.Raw):

  def format(self, value):
    return value.strftime('%Y-%m-%d')

post_errors = {
    "post_001": "List does not exist",
    "post_009": "Post does not exist",
    "post_029": "Image upload failed",
}

post_fields = {
    "post_id": fields.Integer,
    "title": fields.String,
    "hidden": fields.Boolean,
    "img_url": fields.String,
    "created_at": SimpleDateTime,
    "updated_at": SimpleDateTime,
    "creator": {
        "user_id": fields.Integer(attribute='creator.user_id'),
        "email": fields.String(attribute='creator.email'),
        "follows_user": fields.Boolean(attribute='creator.follows_user'),
        "user_follows": fields.Boolean(attribute='creator.user_follows'),
        "is_actually_user": fields.Boolean(attribute='creator.is_actually_user'),
    }
}


post_update_parser = reqparse.RequestParser()
post_update_parser.add_argument('title', type=min_length(1), required=True, trim=True)
post_update_parser.add_argument('content', type=min_length(1), required=True, trim=True)
post_update_parser.add_argument('hidden', type=inputs.boolean, default=False)
post_update_parser.add_argument('coverImage')
post_update_parser.add_argument('fileName', type=min_length(5), required=True, trim=True)

post_create_parser = post_update_parser.copy()

class PostsAPI(Resource):
  method_decorators = [auth_required("token")]

  @marshal_with(post_fields)
  def get(self, post_id):
    post = db.session.query(Post)\
      .filter(Post.post_id == post_id)\
      .filter(Post.creator_id == current_user.user_id or Post.hidden != True)\
      .first()

    if post is None:
      raise NotFoundError(error_code='post_009', error_message=post_errors['post_009'])

    return post.public_view_as_dict(current_user), 200

  def delete(self, post_id):
    post = db.session.query(Post)\
      .filter(Post.post_id == post_id and Post.creator_id == current_user.user_id)\
      .first()

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
  def put(self, post_id):
    post = db.session.query(Post)\
      .filter(Post.post_id == post_id and Post.creator_id == current_user.user_id)\
      .first()

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
      post.img_url = image_url
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return post

  @marshal_with(post_fields)
  def post(self):
    args = post_create_parser.parse_args()

    title = args.get('title')
    content = args.get('content')
    hidden = args.get('hidden', False)
    image_base64 = args.get('coverImage', None)
    orignal_filename = args.get('fileName', "unknown.png")

    filename = secure_filename(str(current_user.user_id) + "_" + datetime.now().strftime('%f') + orignal_filename)

    try:
      with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as f:
        f.write(base64.decodebytes(image_base64.encode()))
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='post_029', error_message=post_errors['post_029'])

    try:
      new_post = Post(title=title, content=content, hidden=hidden, creator=current_user, img_url=filename)
      db.session.add(new_post)
      db.session.commit()
    except Exception as e:
      app.log_exception(e)
      db.session.rollback()
      raise InternalServerError(error_code='common_001', error_message=common_errors['common_001'])

    return new_post
