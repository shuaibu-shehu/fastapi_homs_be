from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from lib.middleware import register_middleware
from lib.errors import AccessTokenRequired, HospitalAlreadyExists, HospitalNotFound, InsufficientPermission, InvalidCredentials, InvalidToken, RefreshTokenRequired, RevokedToken, UserAlreadyExists, UserNotFound, create_exception_handler, register_error_handlers
from routes import (auth_router,
                    user_router,
                    hospital_router,
                    department_router)
import uvicorn
from config.config import Config
from config.connection import db 


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@asynccontextmanager
async def lifespan(app: FastAPI):    
    try:
        # Attempt to connect to the database
        await db.connect()
    except Exception as e:
        # Log the error and proceed without crashing the app
        print(f"Failed to connect to the database: {e}")
    
    yield

    # Attempt to disconnect from the database, if connected
    try:
        await db.disconnect()
    except Exception as e:
        print(f"Failed to disconnect from the database: {e}")
VERSION="v1"


def init_app():
    app = FastAPI(
        title="Lecdmon code 21",
        description="Fast API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=f"/api/{VERSION}/docs",
    )

    register_error_handlers(app)

    register_middleware(app) 

    app.include_router(auth_router, prefix=f"/api/{VERSION}/auth", tags=["auth"])
    app.include_router(user_router, prefix=f"/api/{VERSION}/user", tags=["user"])
    app.include_router(hospital_router, prefix=f"/api/{VERSION}/hospital", tags=["hospital"])
    app.include_router(department_router, prefix=f"/api/{VERSION}/departments", tags=["departments"])


    @app.get(f'/api/{VERSION}')
    def home():
        return {"message":"welcome to fast api"}
    
    return app

app = init_app()
   
if __name__ == '__main__':
    uvicorn.run("main:app",
                 host="localhost",
                 port=8888,
                 reload=True,
                 access_log=False
                 ) 