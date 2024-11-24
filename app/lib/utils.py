from enum import Enum
# app/services/auth_service.py
from datetime import timedelta, timezone
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
import random
import string



# Constant for JWT token
ACCESS_TOKEN_EXPIRE = 2

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
    )

# Helper functions
def generate_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta=None, refresh:bool=False, is_email_verification:bool=False):
    payload = data.copy()
    expire = datetime.now() + (expires_delta if expires_delta is not None else timedelta(days=ACCESS_TOKEN_EXPIRE))
    
    payload.update({"exp": expire})
    
    payload.update({"jti": str(uuid.uuid4())})
    
    payload.update({"refresh": refresh})
    
    payload.update({"is_email_verification": is_email_verification})

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


def token_expired(timestamp)->bool:
    exp_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    exp_time= datetime.time(exp_time)
    current_time = datetime.time(datetime.now())
    print("exp time: ",exp_time, "current time: ",current_time)
    return exp_time < current_time
      

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



class Role(str, Enum):
    NURSE = "nurse"
    ADMIN = "admin"
    DOCTOR = "doctor"
    TECHNICIAN = "technician"
