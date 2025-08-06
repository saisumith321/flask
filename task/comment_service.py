from modules.application.common.types import PaginationResult
from modules.task.internal.comment_reader import CommentReader
from modules.task.internal.comment_writer import CommentWriter
from modules.task.types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetTaskCommentsParams,
    UpdateCommentParams,
)


class CommentService:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        comment_writer = CommentWriter()
        return comment_writer.create_comment(params=params)

    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        comment_reader = CommentReader()
        return comment_reader.get_comment(params=params)

    @staticmethod
    def get_task_comments(*, params: GetTaskCommentsParams) -> PaginationResult[Comment]:
        comment_reader = CommentReader()
        return comment_reader.get_task_comments(params=params)

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        comment_writer = CommentWriter()
        return comment_writer.update_comment(params=params)

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> CommentDeletionResult:
        comment_writer = CommentWriter()
        return comment_writer.delete_comment(params=params)