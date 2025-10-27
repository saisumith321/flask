import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson.objectid import ObjectId

from modules.task.internal.comment_writer import CommentWriter
from modules.task.types import (
    Comment,
    CreateCommentParams,
    UpdateCommentParams,
    DeleteCommentParams,
    CommentDeletionResult,
)
from modules.task.errors import CommentNotFoundError, TaskNotFoundError


class TestCommentWriter:
    """Test suite for CommentWriter"""

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
    def sample_task_bson(self):
        """Sample task BSON data"""
        return {
            "_id": ObjectId("507f1f77bcf86cd799439012"),
            "account_id": "account123",
            "title": "Test Task",
            "description": "Test Description",
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
    def create_comment_params(self):
        """Sample create comment parameters"""
        return CreateCommentParams(
            task_id="507f1f77bcf86cd799439012",
            account_id="account123",
            content="This is a test comment",
            author_name="John Doe"
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

    @patch('modules.task.internal.store.task_repository.TaskRepository.collection')
    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    @patch('modules.task.internal.comment_util.CommentUtil.convert_comment_bson_to_comment')
    @patch('modules.task.internal.store.comment_model.CommentModel')
    def test_create_comment_success(self, mock_model, mock_util, mock_comment_collection, mock_task_collection, 
                                   sample_task_bson, sample_comment_bson, sample_comment, create_comment_params):
        """Test successful comment creation"""
        # Arrange
        mock_task_collection.return_value.find_one.return_value = sample_task_bson
        
        mock_insert_result = Mock()
        mock_insert_result.inserted_id = ObjectId("507f1f77bcf86cd799439011")
        mock_comment_collection.return_value.insert_one.return_value = mock_insert_result
        mock_comment_collection.return_value.find_one.return_value = sample_comment_bson
        
        mock_model.return_value.to_bson.return_value = sample_comment_bson
        mock_util.return_value = sample_comment

        # Act
        result = CommentWriter.create_comment(params=create_comment_params)

        # Assert
        assert result == sample_comment
        mock_task_collection.return_value.find_one.assert_called_once_with({
            "_id": ObjectId(create_comment_params.task_id),
            "account_id": create_comment_params.account_id,
            "active": True
        })
        mock_comment_collection.return_value.insert_one.assert_called_once()
        mock_util.assert_called_once_with(sample_comment_bson)

    @patch('modules.task.internal.store.task_repository.TaskRepository.collection')
    def test_create_comment_task_not_found(self, mock_task_collection, create_comment_params):
        """Test comment creation when task doesn't exist"""
        # Arrange
        mock_task_collection.return_value.find_one.return_value = None

        # Act & Assert
        with pytest.raises(TaskNotFoundError) as exc_info:
            CommentWriter.create_comment(params=create_comment_params)
        
        assert str(exc_info.value) == f"Task with id {create_comment_params.task_id} not found."

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    @patch('modules.task.internal.comment_util.CommentUtil.convert_comment_bson_to_comment')
    def test_update_comment_success(self, mock_util, mock_collection, sample_comment_bson, sample_comment, update_comment_params):
        """Test successful comment update"""
        # Arrange
        updated_comment_bson = {**sample_comment_bson, "content": "Updated comment content"}
        updated_comment = Comment(
            id=sample_comment.id,
            task_id=sample_comment.task_id,
            account_id=sample_comment.account_id,
            content="Updated comment content",
            author_name=sample_comment.author_name,
            created_at=sample_comment.created_at,
            updated_at=datetime(2024, 1, 1, 13, 0, 0),
        )
        
        mock_collection.return_value.find_one_and_update.return_value = updated_comment_bson
        mock_util.return_value = updated_comment

        # Act
        result = CommentWriter.update_comment(params=update_comment_params)

        # Assert
        assert result == updated_comment
        assert result.content == "Updated comment content"
        mock_collection.return_value.find_one_and_update.assert_called_once()
        mock_util.assert_called_once_with(updated_comment_bson)

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    def test_update_comment_not_found(self, mock_collection, update_comment_params):
        """Test comment update when comment doesn't exist"""
        # Arrange
        mock_collection.return_value.find_one_and_update.return_value = None

        # Act & Assert
        with pytest.raises(CommentNotFoundError) as exc_info:
            CommentWriter.update_comment(params=update_comment_params)
        
        assert str(exc_info.value) == f"Comment with id {update_comment_params.comment_id} not found."

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    @patch('modules.task.internal.comment_reader.CommentReader.get_comment')
    def test_delete_comment_success(self, mock_reader, mock_collection, sample_comment, delete_comment_params):
        """Test successful comment deletion"""
        # Arrange
        mock_reader.return_value = sample_comment
        
        deleted_comment_bson = {**sample_comment.__dict__, "active": False}
        mock_collection.return_value.find_one_and_update.return_value = deleted_comment_bson

        # Act
        result = CommentWriter.delete_comment(params=delete_comment_params)

        # Assert
        assert isinstance(result, CommentDeletionResult)
        assert result.comment_id == delete_comment_params.comment_id
        assert result.success is True
        assert isinstance(result.deleted_at, datetime)
        
        mock_reader.assert_called_once()
        mock_collection.return_value.find_one_and_update.assert_called_once()

    @patch('modules.task.internal.store.comment_repository.CommentRepository.collection')
    @patch('modules.task.internal.comment_reader.CommentReader.get_comment')
    def test_delete_comment_not_found_after_read(self, mock_reader, mock_collection, sample_comment, delete_comment_params):
        """Test comment deletion when comment is not found during deletion"""
        # Arrange
        mock_reader.return_value = sample_comment
        mock_collection.return_value.find_one_and_update.return_value = None

        # Act & Assert
        with pytest.raises(CommentNotFoundError) as exc_info:
            CommentWriter.delete_comment(params=delete_comment_params)
        
        assert str(exc_info.value) == f"Comment with id {delete_comment_params.comment_id} not found."