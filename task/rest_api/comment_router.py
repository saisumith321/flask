from flask import Blueprint

from modules.task.rest_api.comment_view import CommentView

comment_router = Blueprint("comment", __name__)

# Routes for comments within tasks
# POST /tasks/{task_id}/comments - Create comment
# GET /tasks/{task_id}/comments - Get all comments for task
# GET /tasks/{task_id}/comments/{comment_id} - Get specific comment
# PATCH /tasks/{task_id}/comments/{comment_id} - Update comment
# DELETE /tasks/{task_id}/comments/{comment_id} - Delete comment

comment_view = CommentView.as_view("comment_view")

comment_router.add_url_rule(
    "/tasks/<task_id>/comments",
    view_func=comment_view,
    methods=["POST", "GET"],
    defaults={"comment_id": None}
)

comment_router.add_url_rule(
    "/tasks/<task_id>/comments/<comment_id>",
    view_func=comment_view,
    methods=["GET", "PATCH", "DELETE"]
)