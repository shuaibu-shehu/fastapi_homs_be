from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from lib.error_logger import error_logger
from models.user import UserLoginModel
from lib.redis import add_jti_to_blocklist
from services.auth_service import AuthService
from lib.dependencies import AccessTokenBearer, VerificationTokenBearer
from controllers import AuthController
from models import UserCreateModel
from fastapi import status
router = APIRouter()

 
verification_token_bearer= VerificationTokenBearer()
auth_service= AuthService()

@router.post("/signup", status_code=status.HTTP_201_CREATED)    
async def signup(user_create: UserCreateModel, auth_controller: AuthController=Depends(AuthController)):
    return  await auth_controller.signup_user(user_create) 

@router.get("/verify")
async def verify(tokenId: Optional[str]="",
                  auth_controller: AuthController=Depends(AuthController),
                  token_details= Depends(verification_token_bearer)
                  ):
    try:
        return  await  auth_controller.verify_email(token_details)
    
    except Exception as e:
        error_logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/logout")
async def revoke_token(token: str, token_details: dict=Depends(AccessTokenBearer)):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Logged Out successfully"}
                        )


@router.post("/login")
async def login(user_data: UserLoginModel, auth_controller: AuthController=Depends(AuthController)):
    return  await auth_controller.login_user(user_data)
 