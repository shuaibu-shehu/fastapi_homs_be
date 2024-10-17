from fastapi import APIRouter, Depends

from controllers import UserController
# from ..services.auth_service import  signup_user
from models import  UserLoginModel
# from app.models.user import User
# from app.services.auth_service import get_current_user
from fastapi import status
router = APIRouter()

 
@router.post("/login", status_code=status.HTTP_201_CREATED)    
async def login(user_data: UserLoginModel, user_controller: UserController=Depends(UserController)):
    return  await user_controller.login_user(user_data) 



