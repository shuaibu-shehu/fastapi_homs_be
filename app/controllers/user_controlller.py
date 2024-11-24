from fastapi import HTTPException, status
from lib import error_logger
from lib.errors import InvalidCredentials
from lib.utils import create_access_token, verify_password
from services import UserService, HospitalService
from datetime import timedelta
from  fastapi.responses import JSONResponse

user_service = UserService()    
hospital_service = HospitalService()

REFRESH_TOKEN_EXPIRY=2
class UserController:

    async def login_user(self, user_data):
        try:
            existing_user = await user_service.get_user_by_email(user_data.email)
            if not existing_user:
                raise InvalidCredentials()
            verify = verify_password(user_data.password, existing_user.password)
            
            if not verify:
                raise InvalidCredentials()
            access_token = create_access_token(
                data={
                    "email": existing_user.email,
                    "user_uid": str(existing_user.id)
                    })
           
            refresh_token = create_access_token(
                data={
                    "email": existing_user.email,
                    "user_uid": str(existing_user.id)
                    },
                    expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRY),
                    refresh=True,
                    )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "login success",
                    "access_token": access_token,
                    "token_type": "bearer",
                    "refresh_token": refresh_token,
                    "user":{
                        "email": existing_user.email,
                        "uid": str(existing_user.id)
                        }
                        }
                    )
        except Exception as e:
              error_logger.error(e)
              raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
 
 
    async def get_users_by_hospital_id(self, hospital_id: str, email: str):
        try:
            hospital = await hospital_service.get_hospital_by_id(hospital_id)
            if not hospital:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
            return await user_service.get_users_by_hospital_id(hospital_id)
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    