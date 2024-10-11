# app/services/auth_service.py

from datetime import timedelta
from passlib.context import CryptContext
# from jose import jwt
from config.connection import db
from lib.utils import create_access_token, get_password_hash
from models.user import UserCreate, User
from fastapi import HTTPException

async def signup_user_service(user_create):
    print(user_create)
    try:
        user_data = {
        "name": user_create.username,
        "email": user_create.email,
        "password": user_create.password,
    }
 
        # print("data:",user_data)

        user = await db.prisma.user.create({**user_data})

    # Store user in "database"
    # Here, replace with actual DB insertion
    
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"messsage": "user created"}
    # return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
   

async def get_user_by_email(email: str):
    user = await db.prisma.user.find_unique(
        where={
            "email": email
        }
    )
    return user