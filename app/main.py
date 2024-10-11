from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from routes import auth_routes
import uvicorn
# from .services.test import say_hello

from config.connection import db 
# app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
    docs_url="/api/v1/docs"

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    try:
        # Attempt to connect to the database
        await db.connect()
        print("Connected to the database")
    except Exception as e:
        # Log the error and proceed without crashing the app
        print(f"Failed to connect to the database: {e}")
    
    yield

    # Attempt to disconnect from the database, if connected
    try:
        await db.disconnect()
        print("Disconnected from the database")
    except Exception as e:
        print(f"Failed to disconnect from the database: {e}")
VERSION="v1"
def init_app():
    apps = FastAPI(
        title="Lemon code 21",
        description="Fast API",
        version="1.0.0",
        lifespan=lifespan
    )


    apps.include_router(auth_routes.router, prefix=f"/api/{VERSION}/auth")
 
    @apps.get(f'/api/{VERSION}')
    def home():
        return {"message":"welcome to fast api"}
    
    return apps
 
app = init_app()
  
if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)