from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from modules.application.base_repository import BaseRepository
from modules.application.common.types import PaginationParams, PaginationResult
from modules.task.internal.store.comment_model import CommentModel


class CommentRepository(BaseRepository[CommentModel]):
    def __init__(self):
        super().__init__(model_class=CommentModel)

    def create_comment(self, comment_model: CommentModel) -> CommentModel:
        comment_model.created_at = datetime.now()
        comment_model.updated_at = datetime.now()
        return self.create(comment_model)

    def get_comment_by_id(self, comment_id: str, task_id: str, account_id: str) -> Optional[CommentModel]:
        query = {
            "_id": ObjectId(comment_id),
            "task_id": task_id,
            "account_id": account_id,
            "active": True
        }
        return self.find_one(query)

    def get_comments_by_task_id(
        self, 
        task_id: str, 
        account_id: str, 
        pagination_params: PaginationParams
    ) -> PaginationResult[CommentModel]:
        query = {
            "task_id": task_id,
            "account_id": account_id,
            "active": True
        }
        sort_params = [("created_at", -1)]  # Sort by newest first
        
        return self.find_paginated(
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params
        )

    def update_comment(self, comment_id: str, task_id: str, account_id: str, update_data: dict) -> Optional[CommentModel]:
        query = {
            "_id": ObjectId(comment_id),
            "task_id": task_id,
            "account_id": account_id,
            "active": True
        }
        update_data["updated_at"] = datetime.now()
        return self.update_one(query, {"$set": update_data})

    def delete_comment(self, comment_id: str, task_id: str, account_id: str) -> bool:
        query = {
            "_id": ObjectId(comment_id),
            "task_id": task_id,
            "account_id": account_id,
            "active": True
        }
        update_data = {
            "active": False,
            "updated_at": datetime.now()
        }
        result = self.update_one(query, {"$set": update_data})
        return result is not None