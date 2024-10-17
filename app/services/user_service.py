from datetime import timedelta
# from passlib.context import CryptContext
# from jose import jwt
from config.connection import db
# from lib.utils import create_access_token, get_password_hash
from models import UserCreateModel, User
from fastapi import HTTPException

class UserService:
       
       async def login_user(self, user_data):
        print(user_data)
        return

       async def get_user_by_email(self,email: str):
        user = await db.prisma.user.find_unique(
            where={
                "email": email
            }
        )
        return user
       