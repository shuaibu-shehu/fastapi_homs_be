

from fastapi import Depends


from fastapi import HTTPException, status
from lib.errors import InsufficientPermission
from models.user import User
from services import UserService
from typing import List, Any

user_service = UserService()

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(user_service.get_current_user)) -> Any:
        print(current_user.role)
        if current_user.role in self.allowed_roles:
            return True

        raise InsufficientPermission()
    