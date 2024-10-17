# app/services/auth_service.py
from datetime import timedelta
import os
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
# from models.user import UserCreate
from config.config import Config
from datetime import datetime
import uuid 
import logging
import config.connection as db


# Constant for JWT token
ACCESS_TOKEN_EXPIRE = 3600

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
    )

# Helper functions
def generate_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta=None, refresh:bool=False):
    payload = data.copy()
    print(expires_delta)
    print(Config.JWT_ALGORITHM)
    expire = datetime.now() + (expires_delta if expires_delta is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRE))
    
    payload.update({"exp": expire})
    
    payload.update({"jti": str(uuid.uuid4())})
    
    payload.update({"refresh": refresh})
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET, 
        algorithm=Config.JWT_ALGORITHM
        )  
    
    return token
  

def decode_token(token:str)->dict:
        try:
            token_data=jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
            )

            return token_data
        except jwt.PyJWTError as e:
            logging.exception(e)
            return None    

# async def get_token_by_id(id: str):
#  return db.prisma.verificationtoken.find_unique(where={"id": id})         