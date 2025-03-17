from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from lib.websocket_endpoint import websocket_endpoint
from lib.middleware import register_middleware
from lib.errors import register_error_handlers
from routes import (auth_router,
                    user_router,
                    hospital_router,
                    department_router,
                    oxygen_router,
                    bed_router)
import uvicorn
from config.config import Config
from config.connection import db 
import asyncio
import random
from datetime import datetime




class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

    
connected_clients = []

# WebSocket Functions
async def notify_clients(data: dict):
    """Notify all connected WebSocket clients with the given data."""
    for client in connected_clients:
        try:
            await client.send_json(data)
        except Exception as e:
            print(f"error: {e}")
            connected_clients.remove(client)


async def simulate_sensor_data():
    """Simulate and broadcast oxygen consumption data for multiple beds."""
    while True:
        flow_rate = round(random.uniform(3.0, 7.0), 2)
        duration = random.randint(1, 10)
        timestamp = datetime.now()

        data = {
            "timestamp": timestamp.isoformat(),
            "flow_rate": flow_rate,
            "duration": duration
        }
        await notify_clients(data)
        
        await asyncio.sleep(random.randint(5, 10))
 
@asynccontextmanager
async def lifespan(app: FastAPI):      
    try:
        await db.connect()
        # Start the simulation task
        # asyncio.create_task(simulate_sensor_data()) 
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
    
    yield
 
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
    # app.include_router(oxygen_router, prefix=f"/api/{VERSION}/oxygen", tags=["oxygen"])
    app.include_router(bed_router, prefix=f"/api/{VERSION}/beds", tags=["beds"])

    websocket_endpoint(app)

    # @app.websocket("/ws/oxygen-updates")
    # async def websocket_endpoint(websocket: WebSocket):  # noqa: F401
    #     await websocket.accept()
    #     print("connected")
    #     connected_clients.append(websocket)
    #     try:
    #         while True:
    #             await websocket.receive_text()
    #     except WebSocketDisconnect:
    #         print("disconnected")
    #         connected_clients.remove(websocket)


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