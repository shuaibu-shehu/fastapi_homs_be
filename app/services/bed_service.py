from datetime import timedelta
import datetime
from typing import Optional
from config.connection import db


class BedService:
    async def create_bed(self, department_id: str, bed_details: dict):
        print(department_id, bed_details)
        await db.prisma.bed.create(
            data= {"bed_number": bed_details["bed_number"],"sensor_id": bed_details["sensor_id"], "department_id": department_id}
        )
        pass
    
    async def get_beds_by_department_id(self, department_id: str):
        return await db.prisma.bed.find_many(where={"department_id": department_id}, include={"daily_consumptions": True})

    async def get_bed_by_id(self, bed_id: str):
        return await db.prisma.bed.find_unique(where={"id": bed_id})
    
    async def get_daily_consumption(self, bed_id: str, start_date: str, end_date: str):
        print("dates", start_date, end_date)

        try:
            if end_date is None:
                next_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                next_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)

            return await db.prisma.dailyoxygenconsumption.find_many(where={
                "bed_id": bed_id, 
                "date": {"gte": start_date, "lte": next_date}
            })
        except Exception as e:
            print("error", e)
            return []
    
    async def delete_bed(self, bed_id: str):
        return await db.prisma.bed.delete(where={"id": bed_id})

    async def get_sensor_data(self, bed_id: str, daily_consumption_id: str):
        try:
            return await db.prisma.sensorreading.find_many(
                where={
                    "bed_id": bed_id,
                    "daily_consumption_id": daily_consumption_id
                }
            )
        except Exception as e:
            print("error", e)
            return []

    async def get_daily_consumptions_by_bed_id(self, bed_id: str):
        return await db.prisma.dailyoxygenconsumption.find_many(where={"bed_id": bed_id})
    

    async def get_daily_consumptions_by_department_id(self, department_id: str, date: Optional[str] = None):
        if date is None:
            return await db.prisma.dailyoxygenconsumption.find_many(where={"bed": {"department_id": department_id}})
        return await db.prisma.dailyoxygenconsumption.find_many(
            where={
                "bed": {
                    "department_id": department_id
                },
                "date": date
            }
        )
    
    async def get_total_consumption_by_department_id(self, department_id: str):
        return await db.prisma.dailyoxygenconsumption.find_many(where={"bed": {"department_id": department_id}})
    
 


