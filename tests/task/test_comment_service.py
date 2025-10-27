import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from modules.task.comment_service import CommentService
from modules.task.types import (
    Comment,
    CreateCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
    DeleteCommentParams,
    CommentDeletionResult,
)
from modules.application.common.types import PaginationParams, PaginationResult


class TestCommentService:
    """Test suite for CommentService"""

    @pytest.fixture
    def sample_comment(self):
        """Sample comment for testing"""
        return Comment(
            id="507f1f77bcf86cd799439011",
            task_id="507f1f77bcf86cd799439012",
            account_id="account123",
            content="This is a test comment",
            author_name="John Doe",
            created_at=datetime(2024, 1, 1, 12, 0, 0),
            updated_at=datetime(2024, 1, 1, 12, 0, 0),
        )

    @pytest.fixture
    def create_comment_params(self):
        """Sample create comment parameters"""
        return CreateCommentParams(
            task_id="507f1f77bcf86cd799439012",
            account_id="account123",
            content="This is a test comment",
            author_name="John Doe"
        )

    @pytest.fixture
    def get_comment_params(self):
        """Sample get comment parameters"""
        return GetCommentParams(
            account_id="account123",
            task_id="507f1f77bcf86cd799439012",
            comment_id="507f1f77bcf86cd799439011"
        )

    @pytest.fixture
    def update_comment_params(self):
        """Sample update comment parameters"""
        return UpdateCommentParams(
            account_id="account123",
            task_id="507f1f77bcf86cd799439012",
            comment_id="507f1f77bcf86cd799439011",
            content="Updated comment content"
        )

    @pytest.fixture
    def delete_comment_params(self):
        """Sample delete comment parameters"""
        return DeleteCommentParams(
            account_id="account123",
            task_id="507f1f77bcf86cd799439012",
            comment_id="507f1f77bcf86cd799439011"
        )

    @patch('modules.task.internal.comment_writer.CommentWriter.create_comment')
    def test_create_comment_success(self, mock_writer, sample_comment, create_comment_params):
        """Test successful comment creation"""
        # Arrange
        mock_writer.return_value = sample_comment

        # Act
        result = CommentService.create_comment(params=create_comment_params)

        # Assert
        assert result == sample_comment
        mock_writer.assert_called_once_with(params=create_comment_params)

    @patch('modules.task.internal.comment_reader.CommentReader.get_comment')
    def test_get_comment_success(self, mock_reader, sample_comment, get_comment_params):
        """Test successful comment retrieval"""
        # Arrange
        mock_reader.return_value = sample_comment

        # Act
        result = CommentService.get_comment(params=get_comment_params)

        # Assert
        assert result == sample_comment
        mock_reader.assert_called_once_with(params=get_comment_params)

    @patch('modules.task.internal.comment_reader.CommentReader.get_paginated_comments')
    def test_get_paginated_comments_success(self, mock_reader, sample_comment):
        """Test successful paginated comments retrieval"""
        # Arrange
        pagination_params = PaginationParams(page=1, size=10, offset=0)
        get_params = GetPaginatedCommentsParams(
            account_id="account123",
            task_id="507f1f77bcf86cd799439012",
            pagination_params=pagination_params
        )
        
        expected_result = PaginationResult(
            items=[sample_comment],
            pagination_params=pagination_params,
            total_count=1,
            total_pages=1
        )
        mock_reader.return_value = expected_result

        # Act
        result = CommentService.get_paginated_comments(params=get_params)

        # Assert
        assert result == expected_result
        mock_reader.assert_called_once_with(params=get_params)

    @patch('modules.task.internal.comment_writer.CommentWriter.update_comment')
    def test_update_comment_success(self, mock_writer, sample_comment, update_comment_params):
        """Test successful comment update"""
        # Arrange
        updated_comment = Comment(
            id=sample_comment.id,
            task_id=sample_comment.task_id,
            account_id=sample_comment.account_id,
            content="Updated comment content",
            author_name=sample_comment.author_name,
            created_at=sample_comment.created_at,
            updated_at=datetime(2024, 1, 1, 13, 0, 0),
        )
        mock_writer.return_value = updated_comment

        # Act
        result = CommentService.update_comment(params=update_comment_params)

        # Assert
        assert result == updated_comment
        assert result.content == "Updated comment content"
        mock_writer.assert_called_once_with(params=update_comment_params)

    @patch('modules.task.internal.comment_writer.CommentWriter.delete_comment')
    def test_delete_comment_success(self, mock_writer, delete_comment_params):
        """Test successful comment deletion"""
        # Arrange
        expected_result = CommentDeletionResult(
            comment_id="507f1f77bcf86cd799439011",
            deleted_at=datetime(2024, 1, 1, 14, 0, 0),
            success=True
        )
        mock_writer.return_value = expected_result

        # Act
        result = CommentService.delete_comment(params=delete_comment_params)

        # Assert
        assert result == expected_result
        assert result.success is True
        mock_writer.assert_called_once_with(params=delete_comment_params)