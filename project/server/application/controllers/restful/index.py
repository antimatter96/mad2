from flask_restful import Api

from application.controllers.restful.post import PostsAPI
from application.controllers.restful.followers import FollowersAPI

api = Api()
api.add_resource(PostsAPI, "/api/post", "/api/post/<int:post_id>")
api.add_resource(FollowersAPI, "/api/followers", "/api/followers/<int:other_user_id>")
