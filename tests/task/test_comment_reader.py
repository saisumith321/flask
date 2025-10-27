import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson.objectid import ObjectId

from modules.task.internal.comment_reader import CommentReader
from modules.task.types import (
    Comment,
    GetCommentParams,
    GetPaginatedCommentsParams,
)
from modules.application.common.types import PaginationParams, PaginationResult
from modules.task.errors import CommentNotFoundError


class TestCommentReader:
    """Test suite for CommentReader"""

    @pytest.fixture
    def sample_comment_bson(self):
        """Sample comment BSON data"""
        return {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "task_id": "507f1f77bcf86cd799439012",
            "account_id": "account123",
            "content": "This is a test comment",
            "author_name": "John Doe",
            "active": True,
            "created_at": datetime(2024, 1, 1, 12, 0, 0),
            "updated_at": datetime(2024, 1, 1, 12, 0, 0),
        }

    @pytest.fixture
    def sample_comment(self):
        """Sample comment object"""
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
    def get_comment_params(self):
        """Sample get comment parameters"""
        return GetCommentParams(
            account_id="account123",
            task_id="507f1f77bcf86cd799439012",
            comment_id="507f1f77bcf86cd799439011"
        )

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    @patch('modules.task.internal.comment_util.CommentUtil.convert_comment_bson_to_comment')
    def test_get_comment_success(self, mock_util, mock_collection, sample_comment_bson, sample_comment, get_comment_params):
        """Test successful comment retrieval"""
        # Arrange
        mock_collection.return_value.find_one.return_value = sample_comment_bson
        mock_util.return_value = sample_comment

        # Act
        result = CommentReader.get_comment(params=get_comment_params)

        # Assert
        assert result == sample_comment
        mock_collection.return_value.find_one.assert_called_once_with({
            "_id": ObjectId(get_comment_params.comment_id),
            "task_id": get_comment_params.task_id,
            "account_id": get_comment_params.account_id,
            "active": True
        })
        mock_util.assert_called_once_with(sample_comment_bson)

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    def test_get_comment_not_found(self, mock_collection, get_comment_params):
        """Test comment not found scenario"""
        # Arrange
        mock_collection.return_value.find_one.return_value = None

        # Act & Assert
        with pytest.raises(CommentNotFoundError) as exc_info:
            CommentReader.get_comment(params=get_comment_params)
        
        assert str(exc_info.value) == f"Comment with id {get_comment_params.comment_id} not found."

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    @patch('modules.task.internal.comment_util.CommentUtil.convert_comment_bson_to_comment')
    @patch('modules.application.common.base_model.BaseModel.calculate_pagination_values')
    def test_get_paginated_comments_success(self, mock_pagination, mock_util, mock_collection, sample_comment_bson, sample_comment):
        """Test successful paginated comments retrieval"""
        # Arrange
        pagination_params = PaginationParams(page=1, size=10, offset=0)
        get_params = GetPaginatedCommentsParams(
            account_id="account123",
            task_id="507f1f77bcf86cd799439012",
            pagination_params=pagination_params
        )

        mock_collection.return_value.count_documents.return_value = 1
        mock_pagination.return_value = (pagination_params, 0, 1)
        
        # Mock cursor chain
        mock_cursor = Mock()
        mock_cursor.sort.return_value = mock_cursor
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = [sample_comment_bson]
        mock_collection.return_value.find.return_value = mock_cursor
        
        mock_util.return_value = sample_comment

        # Act
        result = CommentReader.get_paginated_comments(params=get_params)

        # Assert
        assert isinstance(result, PaginationResult)
        assert result.items == [sample_comment]
        assert result.total_count == 1
        assert result.total_pages == 1
        
        mock_collection.return_value.count_documents.assert_called_once_with({
            "task_id": get_params.task_id,
            "account_id": get_params.account_id,
            "active": True
        })
        mock_collection.return_value.find.assert_called_once()

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    @patch('modules.task.internal.comment_util.CommentUtil.convert_comment_bson_to_comment')
    @patch('modules.application.common.base_model.BaseModel.calculate_pagination_values')
    @patch('modules.application.common.base_model.BaseModel.apply_sort_params')
    def test_get_paginated_comments_with_sort_params(self, mock_sort, mock_pagination, mock_util, mock_collection, sample_comment_bson, sample_comment):
        """Test paginated comments retrieval with custom sort parameters"""
        # Arrange
        pagination_params = PaginationParams(page=1, size=10, offset=0)
        from modules.application.common.types import SortParams
        sort_params = SortParams(field="created_at", direction="desc")
        
        get_params = GetPaginatedCommentsParams(
            account_id="account123",
            task_id="507f1f77bcf86cd799439012",
            pagination_params=pagination_params,
            sort_params=sort_params
        )

        mock_collection.return_value.count_documents.return_value = 1
        mock_pagination.return_value = (pagination_params, 0, 1)
        
        # Mock cursor chain
        mock_cursor = Mock()
        mock_sort.return_value = mock_cursor
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = [sample_comment_bson]
        mock_collection.return_value.find.return_value = mock_cursor
        
        mock_util.return_value = sample_comment

        # Act
        result = CommentReader.get_paginated_comments(params=get_params)

        # Assert
        assert isinstance(result, PaginationResult)
        assert result.items == [sample_comment]
        mock_sort.assert_called_once_with(mock_cursor, sort_params)