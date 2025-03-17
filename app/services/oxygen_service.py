import datetime
from config.connection import db
from lib.error_logger import error_logger

class OxygenService:
   
    async def create_daily_oxygen_entry(self, oxygen_entry: dict):
        return await db.prisma.dailyoxygenconsumption.create(
            data={
                **oxygen_entry
            }
        )
    
    async def record_daily_oxygen_entry(self, staff_id: str, oxygen_entry: dict, department_id: str):
        # daily_oxygen_consumption = await self.create_daily_oxygen_entry(oxygen_entry)
        
        overall_oxygen_consumption = await self.add_to_daily_overall(department_id, oxygen_entry["oxygen_consumption"], oxygen_entry["is_first_time_usage"])
        
        return await db.prisma.individualoxygenconsumption.create(
            data={**oxygen_entry, "nurse_id": staff_id, "department_id": department_id, "daily_oxygen_consumption_id": overall_oxygen_consumption.id}
        )
    

    
    async def update_daily_oxygen_entry(self, oxygen_entry_id: str, oxygen_entry: dict):
        return await db.prisma.individualoxygenconsumption.update(
            where={"id": oxygen_entry_id},
            data={**oxygen_entry}
        )
    
    async def add_to_daily_overall(self, department_id: str, oxygen_consumption: float, is_first_time_usage: bool):
        current_date = f"{datetime.datetime.now().date()}T00:00:00.000Z"

        print("current date : ", current_date)
        # First try to find existing record

        update_data = {
            "total_consumption": {"increment": oxygen_consumption}
        }
        if is_first_time_usage:
            update_data["patients_count"] = {"increment": 1}

        existing_record = await db.prisma.dailyoxygenconsumption.find_first(
            where={
                "department_id": department_id,
                "date": current_date
            }
        )
        
        if existing_record:
            # Update if exists
            
            return await db.prisma.dailyoxygenconsumption.update(
                where={"id": existing_record.id},
                data=update_data
            )
        else:
            # Create if doesn't exist
            return await db.prisma.dailyoxygenconsumption.create(
                data={
                    "department_id": department_id,
                    "total_consumption": oxygen_consumption,
                    "patients_count": 1 
                }
            )
    
    async def subtract_from_daily_overall(self, department_id: str, oxygen_consumption: float, date: str):
        current_date = f"{date}T00:00:00.000Z"
        return await db.prisma.dailyoxygenconsumption.update(
            where={"department_id": department_id, "date": current_date},
            data={"total_consumption": {"decrement": oxygen_consumption}}
        )

    async def get_daily_overall_oxygen_consumption(self, department_id: str, date: str):
        current_date = f"{date}T00:00:00.000Z"
        return await db.prisma.dailyoxygenconsumption.find_first(where={"department_id": department_id, "date": current_date},include={"individualOxygenConsumptions": True})

    async def get_daily_overall_oxygen_consumption_by_id(self,id: str):
        return await db.prisma.dailyoxygenconsumption.find_first(where={"id": id})
    
    async def get_daily_oxygen_entries(self, department_id: str):
        return await db.prisma.individualoxygenconsumption.find_many(where={"department_id": department_id})

    async def delete_daily_oxygen_entry(self, oxygen_entry: dict):
        await db.prisma.dailyoxygenconsumption.update(where={"id": oxygen_entry.daily_oxygen_consumption_id},data={"patients_count": {"decrement": 1},"total_consumption": {"decrement": oxygen_entry.oxygen_consumption}})
        return await db.prisma.individualoxygenconsumption.delete(where={"id": oxygen_entry.id})
    async def get_daily_oxygen_entry_by_id(self, id: str):
        return await db.prisma.individualoxygenconsumption.find_unique(where={"id": id})


