from flask import Blueprint

from modules.task.rest_api.task_router import TaskRouter
from modules.task.rest_api.comment_router import CommentRouter


class TaskRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        task_api_blueprint = Blueprint("task", __name__)
        
        # Add task routes
        task_api_blueprint = TaskRouter.create_route(blueprint=task_api_blueprint)
        
        # Add comment routes
        task_api_blueprint = CommentRouter.create_route(blueprint=task_api_blueprint)
        
        return task_api_blueprint
