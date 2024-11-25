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
        return await db.prisma.individualoxygenconsumption.create(
            data={**oxygen_entry, "staff_id": staff_id, "department_id": department_id}
        )
    
    async def get_daily_oxygen_entries(self, department_id: str):
        return await db.prisma.individualoxygenconsumption.find_many(where={"department_id": department_id})

