from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from lib.middleware import register_middleware
from lib.errors import register_error_handlers
from routes import (auth_router,
                    user_router,
                    hospital_router,
                    department_router,
                    oxygen_router)
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
        except Exception:
            print("error")
            connected_clients.remove(client)

async def simulate_sensor_data():
    """Simulate and broadcast oxygen consumption data for multiple beds."""
    while True:
        bed_number = random.randint(101, 120)
        oxygen_consumption = round(random.uniform(0.5, 5.0), 2)
        is_first_time_usage = random.choice([True, False])
        remarks = "Normal" if oxygen_consumption < 4 else "High usage"
        timestamp = datetime.now()

        data = {
            "department_id": "9f48a932-5280-4431-a326-1583642dbb67",
            "bed_number": bed_number,
            "oxygen_consumption": oxygen_consumption,
            "is_first_time_usage": is_first_time_usage,
            "timestamp": timestamp.isoformat(),
            "remarks": remarks,
        }

        await notify_clients(data)
        await db.prisma.individualoxygenconsumption.create(
            data= {**data, "timestamp": timestamp}
        )
        await asyncio.sleep(random.randint(0, 1))

@asynccontextmanager
async def lifespan(app: FastAPI):    
    try:
        await db.connect()
        # Start the simulation task
        asyncio.create_task(simulate_sensor_data()) 
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
    app.include_router(oxygen_router, prefix=f"/api/{VERSION}/oxygen", tags=["oxygen"])

    @app.websocket("/ws/oxygen-updates")
    async def websocket_endpoint(websocket: WebSocket):  # noqa: F401
        await websocket.accept()
        print("connected")
        connected_clients.append(websocket)
        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            print("disconnected")
            connected_clients.remove(websocket)

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
                 )  #