from datetime import datetime

from modules.task.errors import CommentNotFoundError, CommentTaskNotFoundError
from modules.task.internal.store.comment_model import CommentModel
from modules.task.internal.store.comment_repository import CommentRepository
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    DeleteCommentParams,
    UpdateCommentParams,
)


class CommentWriter:
    def __init__(self):
        self.comment_repository = CommentRepository()
        self.task_repository = TaskRepository()

    def create_comment(self, params: CreateCommentParams) -> Comment:
        # Verify that the task exists and belongs to the account
        task_model = self.task_repository.get_task_by_id(
            task_id=params.task_id,
            account_id=params.account_id
        )
        
        if task_model is None:
            raise CommentTaskNotFoundError(params.task_id)
        
        comment_model = CommentModel(
            task_id=params.task_id,
            account_id=params.account_id,
            content=params.content,
            author=params.author,
        )
        
        created_comment = self.comment_repository.create_comment(comment_model)
        
        return Comment(
            id=str(created_comment.id),
            task_id=created_comment.task_id,
            account_id=created_comment.account_id,
            content=created_comment.content,
            author=created_comment.author,
            created_at=created_comment.created_at,
            updated_at=created_comment.updated_at,
        )

    def update_comment(self, params: UpdateCommentParams) -> Comment:
        # Verify comment exists
        existing_comment = self.comment_repository.get_comment_by_id(
            comment_id=params.comment_id,
            task_id=params.task_id,
            account_id=params.account_id
        )
        
        if existing_comment is None:
            raise CommentNotFoundError(params.comment_id)
        
        update_data = {
            "content": params.content,
        }
        
        updated_comment = self.comment_repository.update_comment(
            comment_id=params.comment_id,
            task_id=params.task_id,
            account_id=params.account_id,
            update_data=update_data
        )
        
        if updated_comment is None:
            raise CommentNotFoundError(params.comment_id)
        
        return Comment(
            id=str(updated_comment.id),
            task_id=updated_comment.task_id,
            account_id=updated_comment.account_id,
            content=updated_comment.content,
            author=updated_comment.author,
            created_at=updated_comment.created_at,
            updated_at=updated_comment.updated_at,
        )

    def delete_comment(self, params: DeleteCommentParams) -> CommentDeletionResult:
        # Verify comment exists before deletion
        existing_comment = self.comment_repository.get_comment_by_id(
            comment_id=params.comment_id,
            task_id=params.task_id,
            account_id=params.account_id
        )
        
        if existing_comment is None:
            raise CommentNotFoundError(params.comment_id)
        
        success = self.comment_repository.delete_comment(
            comment_id=params.comment_id,
            task_id=params.task_id,
            account_id=params.account_id
        )
        
        return CommentDeletionResult(
            comment_id=params.comment_id,
            deleted_at=datetime.now(),
            success=success,
        )