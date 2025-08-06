"""
Validation utilities for task and comment operations
"""
from typing import Any, Dict, List
import re

from modules.task.errors import CommentBadRequestError, TaskBadRequestError


class CommentValidator:
    """Validator for comment operations"""
    
    MAX_CONTENT_LENGTH = 2000
    MIN_CONTENT_LENGTH = 1
    MAX_AUTHOR_NAME_LENGTH = 100
    MIN_AUTHOR_NAME_LENGTH = 1
    
    @classmethod
    def validate_create_comment_data(cls, data: Dict[str, Any]) -> None:
        """Validate data for creating a comment"""
        if not isinstance(data, dict):
            raise CommentBadRequestError("Request data must be a valid JSON object")
        
        # Validate content
        content = data.get("content")
        if not content:
            raise CommentBadRequestError("Content is required")
        
        if not isinstance(content, str):
            raise CommentBadRequestError("Content must be a string")
        
        content = content.strip()
        if len(content) < cls.MIN_CONTENT_LENGTH:
            raise CommentBadRequestError(f"Content must be at least {cls.MIN_CONTENT_LENGTH} character long")
        
        if len(content) > cls.MAX_CONTENT_LENGTH:
            raise CommentBadRequestError(f"Content must not exceed {cls.MAX_CONTENT_LENGTH} characters")
        
        # Validate author name
        author_name = data.get("author_name")
        if not author_name:
            raise CommentBadRequestError("Author name is required")
        
        if not isinstance(author_name, str):
            raise CommentBadRequestError("Author name must be a string")
        
        author_name = author_name.strip()
        if len(author_name) < cls.MIN_AUTHOR_NAME_LENGTH:
            raise CommentBadRequestError(f"Author name must be at least {cls.MIN_AUTHOR_NAME_LENGTH} character long")
        
        if len(author_name) > cls.MAX_AUTHOR_NAME_LENGTH:
            raise CommentBadRequestError(f"Author name must not exceed {cls.MAX_AUTHOR_NAME_LENGTH} characters")
        
        # Check for potentially harmful content
        cls._validate_content_safety(content)
        cls._validate_author_name_format(author_name)
    
    @classmethod
    def validate_update_comment_data(cls, data: Dict[str, Any]) -> None:
        """Validate data for updating a comment"""
        if not isinstance(data, dict):
            raise CommentBadRequestError("Request data must be a valid JSON object")
        
        # Validate content
        content = data.get("content")
        if not content:
            raise CommentBadRequestError("Content is required")
        
        if not isinstance(content, str):
            raise CommentBadRequestError("Content must be a string")
        
        content = content.strip()
        if len(content) < cls.MIN_CONTENT_LENGTH:
            raise CommentBadRequestError(f"Content must be at least {cls.MIN_CONTENT_LENGTH} character long")
        
        if len(content) > cls.MAX_CONTENT_LENGTH:
            raise CommentBadRequestError(f"Content must not exceed {cls.MAX_CONTENT_LENGTH} characters")
        
        # Check for potentially harmful content
        cls._validate_content_safety(content)
    
    @classmethod
    def validate_pagination_params(cls, page: int = None, size: int = None) -> None:
        """Validate pagination parameters"""
        if page is not None:
            if not isinstance(page, int) or page < 1:
                raise CommentBadRequestError("Page must be a positive integer")
            
            if page > 10000:  # Reasonable upper limit
                raise CommentBadRequestError("Page number is too large")
        
        if size is not None:
            if not isinstance(size, int) or size < 1:
                raise CommentBadRequestError("Size must be a positive integer")
            
            if size > 100:  # Reasonable upper limit
                raise CommentBadRequestError("Page size cannot exceed 100")
    
    @classmethod
    def validate_object_id(cls, object_id: str, field_name: str) -> None:
        """Validate MongoDB ObjectId format"""
        if not object_id:
            raise CommentBadRequestError(f"{field_name} is required")
        
        if not isinstance(object_id, str):
            raise CommentBadRequestError(f"{field_name} must be a string")
        
        # MongoDB ObjectId is 24 character hex string
        if len(object_id) != 24:
            raise CommentBadRequestError(f"Invalid {field_name} format")
        
        if not re.match(r'^[0-9a-fA-F]{24}$', object_id):
            raise CommentBadRequestError(f"Invalid {field_name} format")
    
    @classmethod
    def _validate_content_safety(cls, content: str) -> None:
        """Validate content for potentially harmful patterns"""
        # Basic XSS protection
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload\s*=',
            r'onerror\s*=',
            r'onclick\s*=',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                raise CommentBadRequestError("Content contains potentially harmful elements")
        
        # Check for excessive special characters (potential spam)
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s\.\,\!\?\-\(\)]', content)) / len(content)
        if special_char_ratio > 0.3:
            raise CommentBadRequestError("Content contains too many special characters")
    
    @classmethod
    def _validate_author_name_format(cls, author_name: str) -> None:
        """Validate author name format"""
        # Allow letters, numbers, spaces, hyphens, and common punctuation
        if not re.match(r'^[a-zA-Z0-9\s\.\-\']+$', author_name):
            raise CommentBadRequestError("Author name contains invalid characters")
        
        # Check for consecutive spaces or special characters
        if re.search(r'\s{3,}', author_name) or re.search(r'[\.\-\']{2,}', author_name):
            raise CommentBadRequestError("Author name format is invalid")


class TaskValidator:
    """Validator for task operations (extending existing validation)"""
    
    @classmethod
    def validate_task_exists_for_comments(cls, task_id: str, account_id: str) -> None:
        """Validate that task exists and belongs to account before comment operations"""
        cls.validate_object_id(task_id, "Task ID")
        
        if not account_id:
            raise TaskBadRequestError("Account ID is required")
        
        if not isinstance(account_id, str):
            raise TaskBadRequestError("Account ID must be a string")
    
    @classmethod
    def validate_object_id(cls, object_id: str, field_name: str) -> None:
        """Validate MongoDB ObjectId format"""
        if not object_id:
            raise TaskBadRequestError(f"{field_name} is required")
        
        if not isinstance(object_id, str):
            raise TaskBadRequestError(f"{field_name} must be a string")
        
        # MongoDB ObjectId is 24 character hex string
        if len(object_id) != 24:
            raise TaskBadRequestError(f"Invalid {field_name} format")
        
        if not re.match(r'^[0-9a-fA-F]{24}$', object_id):
            raise TaskBadRequestError(f"Invalid {field_name} format")