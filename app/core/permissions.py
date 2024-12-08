from typing import List, Optional
from fastapi import HTTPException, status
from app.models.user_model import User, UserRole, SubscriptionTier

class PermissionDenied(HTTPException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

def check_premium_access(user: User):
    if user.subscription != SubscriptionTier.PREMIUM:
        raise PermissionDenied(
            detail="This feature requires a premium subscription"
        )
    return True

def is_task_owner(user: User, task_user_id: int) -> bool:
    return (
        user.role == UserRole.ADMIN or 
        user.id == task_user_id
    )

class RoleChecker:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User) -> bool:
        if user.role not in self.allowed_roles:
            raise PermissionDenied()
        return True

class TaskPermissions:
    @staticmethod
    def can_create(user: User) -> bool:
        return user.role in [UserRole.ADMIN, UserRole.USER]

    @staticmethod
    def can_read(user: User, task_user_id: Optional[int]) -> bool:
        if user.role == UserRole.ADMIN:
            return True
        return task_user_id is None or user.id == task_user_id

    @staticmethod
    def can_update(user: User, task_user_id: int) -> bool:
        return user.role == UserRole.ADMIN or user.id == task_user_id

    @staticmethod
    def can_delete(user: User, task_user_id: int) -> bool:
        return user.role == UserRole.ADMIN or user.id == task_user_id

    @staticmethod
    def can_manage_tags(user: User) -> bool:
        return user.role == UserRole.ADMIN

admin_only = RoleChecker([UserRole.ADMIN])
authenticated = RoleChecker([UserRole.ADMIN, UserRole.USER]) 