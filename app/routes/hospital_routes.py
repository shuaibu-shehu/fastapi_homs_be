from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from lib.role_checker import RoleChecker
from lib import error_logger
from controllers.auth_controller import AuthController
from lib.dependencies import AccessTokenBearer, VerificationTokenBearer
from controllers import HospitalController
from models import HospitalOnboardModel
# from ..services.auth_service import  signup_user
from models import  UserLoginModel
# from app.models.user import User
# from app.services.auth_service import get_current_user
from fastapi import status
router = APIRouter()


verification_token_bearer= VerificationTokenBearer()

access_token_bearer= AccessTokenBearer()

hospital_controller= HospitalController()

role_checker = RoleChecker(["admin"])

@router.post("/onboard", status_code=status.HTTP_201_CREATED)    
async def onboard(hospital_details: HospitalOnboardModel, hospital_controller: HospitalController=Depends(HospitalController)):
    return  await hospital_controller.onboard(hospital_details) 

@router.get("/verify")
async def verify(tokenId: Optional[str]="",
                  auth_controller: AuthController=Depends(AuthController),
                  token_details= Depends(verification_token_bearer)
                  ):
        try:
            return  await  hospital_controller.verify(token_details)
        
            return {"success":False, "message": "token expired, check your email for new verification link"}
        
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

@router.get("/users/{hospital_id}", dependencies=[Depends(role_checker)])
async def get_users(hospital_id: str, token_details= Depends(access_token_bearer)):
    print(hospital_id)
    return await hospital_controller.get_users(hospital_id, token_details["email"])

@router.get("/{hospital_id}")
async def get_hospital(hospital_id: str, token_details= Depends(access_token_bearer)):
    return await hospital_controller.get_hospital( hospital_id, token_details["email"])

@router.get("/departments/{hospital_id}")
async def get_departments(hospital_id: str, token_details= Depends(access_token_bearer)):
    return await hospital_controller.get_departments(hospital_id, token_details["email"])
 