from datetime import timedelta, timezone
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from lib.error_logger import error_logger
from lib.errors import (InvalidCredentials,
                        UserAlreadyExists,
                        UserNotFound,
                        UserOrHospitalNotFound)
from lib.utils import create_access_token, verify_password
from config.config import Config
from services.user_service import UserService
from models import UserCreateModel
from services import AuthService
from fastapi import status
from jinja2 import Environment, FileSystemLoader
from config.connection import db

 
auth_service = AuthService()

user_service = UserService()

template_env = Environment(loader=FileSystemLoader(Config.TEMPLATE_FOLDER))

REFRESH_TOKEN_EXPIRY=2


email_template = template_env.get_template("welcome_email.html")
class AuthController:
    async def signup_user(self,user_create: UserCreateModel):
            try:   
                existed_user = await user_service.get_user_by_email(user_create.email)
                
                if existed_user: 
                    raise UserAlreadyExists()

                user = await auth_service.signup_user(user_create)
                is_email_verification=True
                
                # html_content = email_template.render(name=user.name, verify_url=verify_url)
                subject = "Email Verification"
                await auth_service.send_email_verification(user,email_template,subject, is_email_verification,email_template)
                return {"success":True, "data": user, "message": "user created successfully, check your email for verification"}
            except Exception as e:
                    error_logger.error(e)
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))         
            
    async def verify_email(self, token_data):
        try:
            # Check if the email belongs to a user
            user = await user_service.get_user_by_email(token_data["email"])
            if user:
                # Verify the user if it exists
                await db.prisma.user.update(
                    where={"id": user.id},
                    data={"verified": True}
                )
                entity = "User"
            
            else:
                # If not a user, check if it's associated with a hospital
                hospital = await db.prisma.hospital.find_unique(
                    where={"email": token_data["email"]}
                )

                if hospital:
                    # Verify the hospital if it exists
                    await db.prisma.hospital.update(
                        where={"id": hospital.id},
                        data={"verified": True}
                    )

                    await user_service.create_hospital_admin(hospital)
                    entity = "Hospital"
                else:
                    # If neither is found, raise an error
                    raise UserOrHospitalNotFound()

            # Delete the verification token
            await db.prisma.verificationtoken.delete(
                where={"token": token_data["token"]}
            )

            return {"success": True, "message": f" {'email verified successfully' if entity == 'User' else 'login credeintials sent to your email'}"}

        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ooops! Something went wrong")

          
    async def login_user(self, user_data):
        try:
            existing_user = await user_service.get_user_by_email(user_data.email)
            if not existing_user:
                raise UserNotFound()
            
            verify = verify_password(user_data.password, existing_user.password)
            if not verify:
                # raise InvalidCredentials()
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                    content={"message":"Invalid credentials"}
                                    )
             
            if not existing_user.verified:
                await auth_service.send_email_verification(existing_user, True)
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                    content={"message":"Email not verified, new confirmation link sent to your email"}
                                    )
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
                    "success": True,
                    "message": "logged successfully",
                    "access_token": access_token,
                    "token_type": "bearer",
                    "refresh_token": refresh_token,
                    "user": {
                        "email": existing_user.email,
                        "uid": str(existing_user.id),
                        "name": existing_user.name,
                        "role": existing_user.role,
                        "department_id": existing_user.departmentId
                    },
                     "hospital": {
                            "id": existing_user.hospital.id,
                            "name": existing_user.hospital.name,
                            "address": existing_user.hospital.address,
                            "city": existing_user.hospital.city,
                            "state": existing_user.hospital.state,
                            "country": existing_user.hospital.country,
                            "contact_number": existing_user.hospital.contact_number,
                            "contact_person": existing_user.hospital.contact_person,
                        }
                }
            )
        except Exception as e:
            #   error_logger.error(e)
              print(e)
              raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")



 
 