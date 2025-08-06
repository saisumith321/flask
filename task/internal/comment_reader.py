from modules.application.common.types import PaginationResult
from modules.task.errors import CommentNotFoundError
from modules.task.internal.store.comment_repository import CommentRepository
from modules.task.types import Comment, GetCommentParams, GetTaskCommentsParams


class CommentReader:
    def __init__(self):
        self.comment_repository = CommentRepository()

    def get_comment(self, params: GetCommentParams) -> Comment:
        comment_model = self.comment_repository.get_comment_by_id(
            comment_id=params.comment_id,
            task_id=params.task_id,
            account_id=params.account_id
        )
        
        if comment_model is None:
            raise CommentNotFoundError(params.comment_id)
        
        return Comment(
            id=str(comment_model.id),
            task_id=comment_model.task_id,
            account_id=comment_model.account_id,
            content=comment_model.content,
            author=comment_model.author,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    def get_task_comments(self, params: GetTaskCommentsParams) -> PaginationResult[Comment]:
        pagination_result = self.comment_repository.get_comments_by_task_id(
            task_id=params.task_id,
            account_id=params.account_id,
            pagination_params=params.pagination_params
        )
        
        comments = [
            Comment(
                id=str(comment_model.id),
                task_id=comment_model.task_id,
                account_id=comment_model.account_id,
                content=comment_model.content,
                author=comment_model.author,
                created_at=comment_model.created_at,
                updated_at=comment_model.updated_at,
            )
            for comment_model in pagination_result.items
        ]
        
        return PaginationResult(
            items=comments,
            page=pagination_result.page,
            size=pagination_result.size,
            total=pagination_result.total,
        )