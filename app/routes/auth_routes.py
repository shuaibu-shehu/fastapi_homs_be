from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends

from lib.dependencies import AccessTokenBearer
from controllers import AuthController
# from ..services.auth_service import  signup_user
from models import UserCreateModel
# from app.models.user import User
# from app.services.auth_service import get_current_user
from fastapi import status
router = APIRouter()


access_token_bearer= AccessTokenBearer()
 
@router.post("/signup", status_code=status.HTTP_201_CREATED)    
async def signup(user_create: UserCreateModel, auth_controller: AuthController=Depends(AuthController)):
    return  await auth_controller.signup_user(user_create) 

@router.get("/verify")
async def verify(tokenId: Optional[str]="",
                  auth_controller: AuthController=Depends(AuthController),
                  token_details= Depends(access_token_bearer)
                  ):
    print("toke details from auth beaer : ",token_details)

    timestams = token_details["exp"]

    time= datetime.fromtimestamp(timestams)
    print("time stamp: ",timestams)
    print("time: ",time)
    # now = datetime.now(tz=timezone.utc)
    now = datetime.now()
    print("now: ",now)
    # return  await auth_controller.verify_user(tokenId)

