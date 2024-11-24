from typing import Any, List
from fastapi import Depends, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from models.user import User
from lib.redis import token_in_blocklist
from services import  AuthService
from .utils import decode_token, token_expired
from fastapi.exceptions import HTTPException
from config.connection import db

 
  
auth_servide = AuthService()
# user_service = UserService()
class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        self.token = creds.credentials

        from services.user_service import UserService
        user_service = UserService()

        token_data = decode_token(self.token)
    
        if not self.token_valid(self.token):
            existing_token = await db.prisma.verificationtoken.find_unique(where={"token": self.token})  
            if existing_token:
                existing_user= await user_service.get_user_by_email(existing_token.email) 
                if existing_user:
                    await auth_servide.send_email_verification(existing_user, True)        
                    await db.prisma.verificationtoken.delete(
                        where={
                            "token": self.token
                        } 
                    )
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail={
                            "error":"This token is invalid or expired",
                            "resolution":"A new Verification Link is sent to your email"
                        }, 
                    )        
            
            
        print("\n\nin blacklist : ",token_data)
        if await token_in_blocklist(token_data['jti']):
            # print("token in blocklist")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error":"This token is invalid or has been revoked",
                    "resolution":"Please get new token"
                }
            )  
        self.verify_token_data(token_data)
        token_data.update({"token": self.token})
        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)
        return (token_data is not None and not token_expired(token_data["exp"])) 

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and (token_data["refresh"] or token_data["is_email_verification"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and (not token_data["refresh"] or token_data["is_email_verification"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )
        
class VerificationTokenBearer(TokenBearer):
    async def verify_token_data(self, token_data: dict) -> None:
        print(token_data)
        if token_data and (not token_data["is_email_verification"] or token_data["refresh"]):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Please provide a verification token",
                    )
        

 
  