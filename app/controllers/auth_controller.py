import asyncio
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from lib.utils import create_access_token, decode_token
from lib.mail import create_message, mail
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
class AuthController:
    async def signup_user(self,user_create: UserCreateModel):
            try:   
                existed_user = await user_service.get_user_by_email(user_create.email)
                
                if existed_user: 
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user already exists")
                
                user = await auth_service.signup_user(user_create)
                token = create_access_token(data={
                                "email": user.email,
                                "user_uid": str(user.id
                                )},
                                 expires_delta=timedelta(seconds=1800)
                                )
                # decoded_token = decode_token(token)            

                saved_token =await db.prisma.verificationtoken.create(
                    data={
                        "email": user.email,
                        "token": token 
                    })
                
                verify_url = f"{Config.FRONTEND_URL}/verify/?id={saved_token.id}"
                template = template_env.get_template("welcome_email.html")
                html_content = template.render(name=user.name, verify_url=verify_url)
                subject = "Welcome to OMS"
                message =  create_message(recipients=[user.email], subject=subject, body=html_content)
                response = await mail.send_message(message)
                print("response: ",response)
                return {"success":True, "data": user, "message": "user created successfully, check your email for verification"}
            except Exception as e:
                    print("error: ",e)
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))         
            
    async def verify_user(self, id: str):
             try:
                print("id user: ",id)
                token_data = await auth_service.verify_token(id)
                print("token data: ",token_data)
                print(datetime.now(timezone.utc))
                # Placeholder code to avoid indentation error
                pass
                # token = await db.prisma.verificationtoken.find_unique(where={"id": id})
                # if not token:
                #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token not found")
                
                # user = await user_service.get_user_by_email(token.email)
                # if not user:
                #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
                
                # token = await db.prisma.verificationtoken.delete(where={"id": id})            
                # return {"message": "verification success", "data": user}        
             except Exception as e:
                  print("error: ",e)
                  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))