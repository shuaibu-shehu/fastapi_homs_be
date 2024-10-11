# app/services/auth_service.py
from datetime import timedelta
import os
from fastapi import HTTPException
from passlib.context import CryptContext
# from jose import jwt
from models.user import UserCreate
from config.connection import db
from datetime import datetime



# Constants for JWT token
SECRET_KEY =  os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper functions
def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    # encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return encoded_jwt

# Signup service

# Login service
async def login_user(user_create: UserCreate):
    user = db.get(user_create.username)
    
    if not user or not pwd_context.verify(user_create.password, user['hashed_password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_create.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user from token
async def get_current_user(token: str):
    # Logic to get the current user from the token
    pass
