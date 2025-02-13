from typing import Optional
from fastapi import HTTPException, status
from services import BedService, DepartmentService

class BedController:
    def __init__(self):
        self.bed_service = BedService()
        self.department_service = DepartmentService()
    async def create_bed(self, department_id: str, bed_details: dict, email: str):        
        try:
            department= await self.department_service.get_department_by_id(department_id)
            if not department:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
            bed= await self.bed_service.create_bed(department_id, bed_details)
            return {"success":True, "message": "Bed created successfully", "data": bed}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    async def get_beds(self, department_id: str):
        try:
            department= await self.department_service.get_department_by_id(department_id)
            if not department:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
            beds= await self.bed_service.get_beds_by_department_id(department_id)
            return {"success":True, "message": "Beds fetched successfully", "data": beds}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        

    async def get_daily_consumption(self, bed_id: str, start_date: str, end_date: str):
        try:
            bed= await self.bed_service.get_bed_by_id(bed_id)
            if not bed:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found")
            
            daily_consumption= await self.bed_service.get_daily_consumption(bed_id, start_date, end_date)
            return {"success":True, "message": "Daily consumption fetched successfully", "data": daily_consumption}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        

    async def delete_bed(self, bed_id: str):
        try:
            bed= await self.bed_service.get_bed_by_id(bed_id)
            if not bed:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found")
            await self.bed_service.delete_bed(bed_id)
            return {"success":True, "message": "Bed deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_sensor_data(self, bed_id: str, date: str):
        try:
            bed= await self.bed_service.get_bed_by_id(bed_id)
            if not bed:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found")
            
            daily_consumption= await self.bed_service.get_daily_consumption(bed_id, date, None)
            if not daily_consumption:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Daily consumption not found")
            
            # print("daily_consumption", daily_consumption)
            
            sensor_data= await self.bed_service.get_sensor_data(bed_id, daily_consumption[0].id)

            return {"success":True, "message": "Sensor data fetched successfully", "data": sensor_data}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


    async  def get_daily_consumptions_by_bed_id(self, bed_id: str):
        try:
            bed = await self.bed_service.get_bed_by_id(bed_id)
            if not bed:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found")
            daily_consumptions= await self.bed_service.get_daily_consumptions_by_bed_id(bed_id)
            return {"success":True, "message": "Daily consumptions fetched successfully", "data": daily_consumptions}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_daily_consumptions_by_department_id(self, department_id: str, date: Optional[str] = None):
        try:
            daily_consumptions= await self.bed_service.get_daily_consumptions_by_department_id(department_id, date)
            return {"success":True, "message": "Daily consumptions fetched successfully", "data": daily_consumptions}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_total_consumption_by_department_id(self, department_id: str):
        try:
            total_consumption= await self.bed_service.get_total_consumption_by_department_id(department_id)
            return {"success":True, "message": "Total consumption fetched successfully", "data": total_consumption}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

