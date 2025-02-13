import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from prisma import Prisma
from datetime import datetime
import asyncio
import random
from typing import List, Dict
from config.connection import db


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, bed_id: str):
        await websocket.accept()
        if bed_id not in self.active_connections:
            self.active_connections[bed_id] = []
        self.active_connections[bed_id].append(websocket)
        print(f"Bed {bed_id} connected. Active connections: {len(self.active_connections[bed_id])}")

    def disconnect(self, websocket: WebSocket, bed_id: str):
        if bed_id in self.active_connections:
            self.active_connections[bed_id].remove(websocket)
            if not self.active_connections[bed_id]:  # Cleanup empty lists
                del self.active_connections[bed_id]

    async def simulate_sensor_reading(self, bed_id: str):
        """Simulate sensor data and send to WebSocket clients."""
        sensor_data = {
            "bed_id": bed_id,
            "oxygen_flow": random.uniform(1.0, 5.0),
            "duration": 0,
            "total_consumption": 0,
            "input_type": "sensor",
            "timestamp": datetime.utcnow().isoformat(),
        }
        start_time = datetime.utcnow()

        while True:
            # Update dynamic fields
            elapsed_time = (datetime.utcnow() - start_time).total_seconds()
            sensor_data["duration"] = int(elapsed_time)
            sensor_data["oxygen_flow"] = round(random.uniform(1.0, 5.0), 2)
            sensor_data["total_consumption"] = round(
                sensor_data["oxygen_flow"] * elapsed_time / 60, 2
            )
            sensor_data["timestamp"] = datetime.utcnow().isoformat()

            # Broadcast to all WebSocket clients for the bed
            await self.broadcast(bed_id, sensor_data)

            # Simulate delay for real-time updates
            await asyncio.sleep(1)

    async def broadcast(self, bed_id: str, data: dict):
        """Send data to all WebSocket clients connected to the specified bed."""
        if bed_id in self.active_connections:
            for websocket in self.active_connections[bed_id]:
                try:
                    await websocket.send_json(data)
                except Exception:
                    self.disconnect(websocket, bed_id)

    async def process_sensor_data(self, data: dict):
        """Handle incoming sensor data."""
        sensor_id = data.get("sensor_id")
        oxygen_flow = data.get("oxygen_flow")
        duration = data.get("duration")
        timestamp = data.get("timestamp")
        input_type = data.get("input_type")
        bed_id = data.get("bed_id")

        # Fetch bed information
        bed = None
        if input_type == "sensor":
            bed = await db.prisma.bed.find_first(where={"sensor_id": sensor_id})
        else:
            bed = await db.prisma.bed.find_first(where={"id": bed_id})

        if not bed:
            print(f"Bed not found for sensor_id: {sensor_id}")
            return

        # Handle daily consumption and readings (same logic as original code)
        today = datetime.now().strftime('%Y-%m-%d')
        daily_consumption = await db.prisma.dailyoxygenconsumption.find_unique(
            where={
                "bed_id_date": {
                    "bed_id": bed.id,
                    "date": today
                }
            }
        )

        if not daily_consumption:
            daily_consumption = await db.prisma.dailyoxygenconsumption.create(
                data={
                    "bed_id": bed.id,
                    "date": today
                }
            )

        total_consumption = float(oxygen_flow) * float(duration)
        await db.prisma.dailyoxygenconsumption.update(
            where={"id": daily_consumption.id},
            data={"total_consumption": daily_consumption.total_consumption + total_consumption}
        )

        await db.prisma.sensorreading.create(
            data={
                "oxygen_flow": float(oxygen_flow),
                "duration": int(duration),
                "timestamp": timestamp,
                "bed_id": bed.id,
                "daily_consumption_id": daily_consumption.id
            }
        )


manager = ConnectionManager()


def websocket_endpoint(app: FastAPI):
    @app.websocket("/ws/beds/{bed_id}")
    async def websocket_endpoint(websocket: WebSocket, bed_id: str):
        await manager.connect(websocket, bed_id)
        try:
            # Start a sensor simulation task for this bed
            # simulation_task = asyncio.create_task(manager.simulate_sensor_reading(bed_id))

            while True:
                # Handle incoming WebSocket messages (if required)
                data = await websocket.receive_json()
                print(f"Received data: {data}")
                await manager.process_sensor_data(data)

        except WebSocketDisconnect:
            print(f"Bed {bed_id} disconnected.")
            manager.disconnect(websocket, bed_id)
        finally:
            # Cancel the simulation task if the WebSocket disconnects
            simulation_task.cancel()
