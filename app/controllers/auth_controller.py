from fastapi import HTTPException
from services.auth_service import get_user_by_email, signup_user_service
from models.user import UserCreate


async def signup_user(user_create: UserCreate):
        try:    
             existed_user = await get_user_by_email(user_create.email)
             
             if existed_user: 
                 raise HTTPException(status_code=400, detail="user already exists")
             
             await signup_user_service(user_create)
             
             return {"message": "user created"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))         
        
     