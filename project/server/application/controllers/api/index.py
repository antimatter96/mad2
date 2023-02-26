from flask_restful import Api

from application.controllers.api.post import PostsAPI
# from application.controllers.api.list import ListAPI

api = Api()
api.add_resource(PostsAPI, "/api/post", "/api/post/<int:post_id>")
# api.add_resource(PostsAPI, "/api/user", "/api/user/<int:user_id")
# api.add_resource(PostsAPI, "/api/follow", "/api/follow/<int:user_id")
# api.add_resource(ListAPI, "/api/list", "/api/list/<int:list_id>")
