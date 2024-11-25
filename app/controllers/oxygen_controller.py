from fastapi import HTTPException, status
from lib.errors import DepartmentNotFound, HospitalNotFound, UserNotFound
from lib.error_logger import error_logger
from services.oxygen_service import OxygenService
from services.department_service import DepartmentService
from services.hospital_service import HospitalService
from services.user_service import UserService
from models import DailyOxygenConsumptionModel

department_service = DepartmentService()
user_service = UserService()
hospital_service = HospitalService()
oxygen_service = OxygenService()

class OxygenController:

    # def __init__(self):
    #     self.oxygen_service = OxygenService()
        
    async def record_daily_oxygen_entry(self, department_id: str, staff_id: str, oxygen_entry: dict, email: str):
        
        try:
            user = await user_service.get_user_by_email(email)
            if not user:
                raise UserNotFound()
           
            department = await department_service.get_department_by_id(department_id=department_id)
            if not department:
                raise DepartmentNotFound()

            hospital = await hospital_service.get_hospital_by_id(department.hospitalId)
            if not hospital:
                raise HospitalNotFound()

            oxygen_consumption = await oxygen_service.record_daily_oxygen_entry(  staff_id=staff_id, oxygen_entry=oxygen_entry,department_id=department_id)
            return {"success":True, "message": "Oxygen consumption recorded successfully", "data": oxygen_consumption}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            

    async def get_daily_oxygen_entries(self, department_id: str, email: str):
        try:
            user = await user_service.get_user_by_email(email)
            if not user:
                raise UserNotFound()
            department = await department_service.get_department_by_id(department_id=department_id)
            if not department:
                raise DepartmentNotFound()
            
            oxygen_entries = await oxygen_service.get_daily_oxygen_entries(department_id=department_id)
            return {"success":True, "message": "Oxygen consumption entries fetched successfully", "data": oxygen_entries}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))       


