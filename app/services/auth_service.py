# app/services/auth_service.py

from datetime import datetime, timedelta, timezone
from jinja2 import Environment, FileSystemLoader
from passlib.context import CryptContext
from lib import error_logger
from lib.errors import InvalidCredentials
from lib.mail import create_message, mail
from lib.utils import create_access_token, decode_token, generate_password_hash
from config.connection import db
from models import UserCreateModel, User
from fastapi import HTTPException, status
from config.config import Config



template_env = Environment(loader=FileSystemLoader(Config.TEMPLATE_FOLDER))
EXPIRY_TIME= 3600

class AuthService:
    async def signup_user(self, user_create:UserCreateModel):
        try:
            hashed_password = generate_password_hash(user_create.password)
            user_data = {
            "name": user_create.username,
            "email": user_create.email,
            "password": hashed_password,
        }
            user = await db.prisma.user.create({**user_data})
            return user 
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))
    
    async def verify_token(self, token_id: str):
        try:
            existing_token = await db.prisma.verificationtoken.find_unique(where={"id": token_id})    
             
            if not existing_token:
                raise InvalidCredentials()

            token_data= decode_token(existing_token.token)
         
            return existing_token
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=400, detail=str(e))
        
    async def send_email_verification(self,
                                      data,
                                      template,
                                      subject: str,
                                      is_email_verification: bool=False
                                      ):
            try:
                token = create_access_token(data={
                                "email": data.email,
                                "user_uid": str(data.id
                                )},
                                 expires_delta=timedelta(seconds=EXPIRY_TIME),
                                 is_email_verification=is_email_verification
                                )

                verify_url = f"{Config.FRONTEND_URL}/new-verification/?token={token}"
                
                html_content = template.render(name=data.name, verify_url=verify_url)
                
                message =  create_message(recipients=[data.email], subject=subject, body=html_content) 
                await mail.send_message(message)
                await db.prisma.verificationtoken.create(data={
                    "token": token,
                    "email": str(data.email)
                })

            except Exception as e:
                     error_logger.error(e)
                     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


 