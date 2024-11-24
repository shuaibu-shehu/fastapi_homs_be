from fastapi import APIRouter, Depends

from lib.dependencies import AccessTokenBearer
from controllers import UserController
# from ..services.auth_service import  signup_user
from models import  UserLoginModel
# from app.models.user import User
# from app.services.auth_service import get_current_user
from fastapi import status
router = APIRouter()

user_controller = UserController()
access_token_bearer = AccessTokenBearer()

@router.post("/login", status_code=status.HTTP_201_CREATED)    
async def login(user_data: UserLoginModel, user_controller: UserController=Depends(UserController)):
    return  await user_controller.login_user(user_data) 

@router.get("/hospital/{hospital_id}")
async def get_users(hospital_id: str,
                    token_details= Depends(access_token_bearer)
                    ):
    print(hospital_id)    
    return await user_controller.get_users_by_hospital_id(hospital_id, token_details["email"]) 

 


