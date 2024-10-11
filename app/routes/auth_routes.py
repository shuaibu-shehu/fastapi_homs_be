from fastapi import APIRouter, Depends

from controllers.auth_controller import signup_user
# from ..services.auth_service import  signup_user
from models.user import UserCreate
# from app.models.user import User
# from app.services.auth_service import get_current_user

router = APIRouter()

 
@router.post("/signup")
async def signup(user_create: UserCreate):
    print(user_create)
    return  await signup_user(user_create) 


# async def signup_user(user_create: UserCreate):
#     hashed_password = get_password_hash(user_create.password)
    
#     # Store user in "database"
#     # Here, replace with actual DB insertion
    
#     # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     # access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
#     return {"access_token": access_token, "token_type": "bearer"}
 