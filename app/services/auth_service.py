# app/services/auth_service.py

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
# from jose import jwt
from lib.utils import decode_token, generate_password_hash
from config.connection import db
# from lib.utils import create_access_token, get_password_hash
from models import UserCreateModel, User
from fastapi import HTTPException


class AuthService:
    async def signup_user(self, user_create:UserCreateModel):
        print(user_create)
        try:
            hashed_password = generate_password_hash(user_create.password)
            print("hasged pass ",hashed_password)
            user_data = {
            "name": user_create.username,
            "email": user_create.email,
            "password": hashed_password,
        }
    
            user = await db.prisma.user.create({**user_data})
            
            return user 
         
        except Exception as e:
            print("error: ",e)
            raise HTTPException(status_code=400, detail=str(e))
    
    async def verify_token(self, token_id: str):
        try:
            existing_token = await db.prisma.verificationtoken.find_unique(where={"id": token_id})    
            
            print("existing token: ",existing_token)
            if not existing_token:
                raise HTTPException(status_code=400, detail="Token not found")
            

            token_data= decode_token(existing_token.token)
            print("token data: ",token_data)
            exp_time = datetime.fromtimestamp(token_data["exp"], tz=timezone.utc)
            print("exp: ",token_data["exp"])
            print("exp time: ",exp_time.astimezone())
            print("now: ",datetime.now())
            print("now time: ",datetime.now(timezone.utc))
            if exp_time < datetime.now(timezone.utc):
                print("token expired")
                # raise HTTPException(status_code=400, detail="Token expired")    
            return existing_token
        except Exception as e:
            print("error: ",e)
            raise HTTPException(status_code=400, detail=str(e))


