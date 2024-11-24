from datetime import timedelta

from lib.dependencies import AccessTokenBearer
from services.auth_service import AuthService
from lib.mail import create_message, mail
from lib.utils import Role, generate_password_hash, generate_random_string
from config.connection import db
from models import UserCreateModel, User
from fastapi import Depends, HTTPException
from config.config import Config
from typing import List, Any
from fastapi import status

auth_service = AuthService()
access_token_bearer = AccessTokenBearer()

class UserService:
    async def get_user_by_email(self, email: str):
        user = await db.prisma.user.find_unique(
            where={
                "email": email
            },
            include={"hospital": True}
        )
        return user

    async def create_hospital_admin(self, hospital):
        random_password = generate_random_string(8)
        hashed_password = generate_password_hash(random_password)
        await db.prisma.user.create(
            data={
                "email": hospital.email,
                "name": hospital.name,
                "verified": True,
                "password": hashed_password,
                "role": Role.ADMIN,
                "hospital": {"connect": {"id": hospital.id}}
            }
        )

        url = f"{Config.FRONTEND_URL}/login"

        body = f"""
        <html>
        <body>
        <p>Dear {hospital.name},</p>
        <p>Your account has been created successfully. Please use the following credentials to log in as the hospital admin:</p>
        <p>Email: {hospital.email}<br>
        Password: {random_password}</p>
        <p>You can log in using the following link:<br>
        <a href="{url}">Login Page</a></p>
        <p>Best regards,<br>
        OHMS</p>
        </body>
        </html>
        """
        message = create_message(
            recipients=[hospital.email],
            subject=f"Admin Password for {hospital.name}",
            body=body
        )
        await mail.send_message(message)

    async def get_current_user(self, token_details: dict = Depends(access_token_bearer)):
        user = await db.prisma.user.find_unique(
            where={
                "email": token_details["email"]
            }
        )
        return user


    async def get_users_by_hospital_id(self, hospital_id: str):
        return await db.prisma.user.find_many(where={"hospital_id": hospital_id})
    
    async def get_user_by_id(self, user_id: str):
        return await db.prisma.user.find_unique(where={"id": user_id})


