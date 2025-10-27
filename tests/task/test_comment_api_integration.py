import pytest
import json
from datetime import datetime
from unittest.mock import patch, Mock

from flask import Flask
from flask.testing import FlaskClient

from modules.task.rest_api.comment_rest_api_server import CommentRestApiServer
from modules.task.types import Comment, CommentDeletionResult
from modules.application.common.types import PaginationResult, PaginationParams


class TestCommentAPIIntegration:
    """Integration tests for Comment REST API endpoints"""

    @pytest.fixture
    def app(self):
        """Create Flask app for testing"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        
        # Register comment blueprint
        comment_blueprint = CommentRestApiServer.create()
        app.register_blueprint(comment_blueprint, url_prefix='/api/v1')
        
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()

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
    def auth_headers(self):
        """Mock authentication headers"""
        return {'Authorization': 'Bearer test-token'}

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    @patch('modules.task.comment_service.CommentService.create_comment')
    def test_create_comment_success(self, mock_service, mock_auth, client, sample_comment, auth_headers):
        """Test successful comment creation via API"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware
        mock_service.return_value = sample_comment

        request_data = {
            "content": "This is a test comment",
            "author_name": "John Doe"
        }

        # Act
        response = client.post(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments',
            data=json.dumps(request_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['id'] == sample_comment.id
        assert response_data['content'] == sample_comment.content
        assert response_data['author_name'] == sample_comment.author_name
        mock_service.assert_called_once()

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    def test_create_comment_missing_content(self, mock_auth, client, auth_headers):
        """Test comment creation with missing content"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware

        request_data = {
            "author_name": "John Doe"
            # Missing content
        }

        # Act
        response = client.post(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments',
            data=json.dumps(request_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    def test_create_comment_missing_author_name(self, mock_auth, client, auth_headers):
        """Test comment creation with missing author name"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware

        request_data = {
            "content": "This is a test comment"
            # Missing author_name
        }

        # Act
        response = client.post(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments',
            data=json.dumps(request_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    @patch('modules.task.comment_service.CommentService.get_comment')
    def test_get_comment_success(self, mock_service, mock_auth, client, sample_comment, auth_headers):
        """Test successful comment retrieval via API"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware
        mock_service.return_value = sample_comment

        # Act
        response = client.get(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments/507f1f77bcf86cd799439011',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['id'] == sample_comment.id
        assert response_data['content'] == sample_comment.content
        mock_service.assert_called_once()

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    @patch('modules.task.comment_service.CommentService.get_paginated_comments')
    def test_get_paginated_comments_success(self, mock_service, mock_auth, client, sample_comment, auth_headers):
        """Test successful paginated comments retrieval via API"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware
        
        pagination_result = PaginationResult(
            items=[sample_comment],
            pagination_params=PaginationParams(page=1, size=10, offset=0),
            total_count=1,
            total_pages=1
        )
        mock_service.return_value = pagination_result

        # Act
        response = client.get(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments?page=1&size=10',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['total_count'] == 1
        assert len(response_data['items']) == 1
        assert response_data['items'][0]['id'] == sample_comment.id
        mock_service.assert_called_once()

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    @patch('modules.task.comment_service.CommentService.get_paginated_comments')
    def test_get_paginated_comments_with_invalid_page(self, mock_service, mock_auth, client, auth_headers):
        """Test paginated comments retrieval with invalid page parameter"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware

        # Act
        response = client.get(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments?page=0',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    @patch('modules.task.comment_service.CommentService.update_comment')
    def test_update_comment_success(self, mock_service, mock_auth, client, sample_comment, auth_headers):
        """Test successful comment update via API"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware
        
        updated_comment = Comment(
            id=sample_comment.id,
            task_id=sample_comment.task_id,
            account_id=sample_comment.account_id,
            content="Updated comment content",
            author_name=sample_comment.author_name,
            created_at=sample_comment.created_at,
            updated_at=datetime(2024, 1, 1, 13, 0, 0),
        )
        mock_service.return_value = updated_comment

        request_data = {
            "content": "Updated comment content"
        }

        # Act
        response = client.patch(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments/507f1f77bcf86cd799439011',
            data=json.dumps(request_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['content'] == "Updated comment content"
        mock_service.assert_called_once()

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    def test_update_comment_missing_content(self, mock_auth, client, auth_headers):
        """Test comment update with missing content"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware

        request_data = {}  # Missing content

        # Act
        response = client.patch(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments/507f1f77bcf86cd799439011',
            data=json.dumps(request_data),
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    @patch('modules.task.comment_service.CommentService.delete_comment')
    def test_delete_comment_success(self, mock_service, mock_auth, client, auth_headers):
        """Test successful comment deletion via API"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware
        
        deletion_result = CommentDeletionResult(
            comment_id="507f1f77bcf86cd799439011",
            deleted_at=datetime(2024, 1, 1, 14, 0, 0),
            success=True
        )
        mock_service.return_value = deletion_result

        # Act
        response = client.delete(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments/507f1f77bcf86cd799439011',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 204
        assert response.data == b''
        mock_service.assert_called_once()

    @patch('modules.authentication.rest_api.access_auth_middleware.access_auth_middleware')
    def test_create_comment_no_request_body(self, mock_auth, client, auth_headers):
        """Test comment creation with no request body"""
        # Arrange
        mock_auth.return_value = lambda f: f  # Bypass auth middleware

        # Act
        response = client.post(
            '/api/v1/accounts/account123/tasks/507f1f77bcf86cd799439012/comments',
            content_type='application/json',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 400