from fastapi import HTTPException, status
from lib.utils import create_access_token, verify_password
from services import UserService
from datetime import timedelta
from  fastapi.responses import JSONResponse

user_service = UserService()    

REFRESH_TOKEN_EXPIRY=2
class UserController:

    async def login_user(self, user_data):
        try:

            existing_user = await user_service.get_user_by_email(user_data.email)
            if not existing_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            verify = verify_password(user_data.password, existing_user.password)
            
            if not verify:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")  
            
            print("verified password",verify)
            access_token = create_access_token(
                data={
                    "email": existing_user.email,
                    "user_uid": str(existing_user.id)
                    })
            print("access token",access_token)
           
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
              print("error: ",e)
              raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    # async def signup_user(self, user_create: UserCreateModel):

    #     await user_service.login_user(user_data)
        
    #     # print(user_data)
    #     return

 
    