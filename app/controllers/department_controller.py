from fastapi import HTTPException,status
from lib.error_logger import error_logger
from services.hospital_service import HospitalService
from lib.errors import (DepartmentAlreadyExists, 
                        HospitalNotFound, 
                        UserNotFound,
                        DepartmentNotFound
                        )
from services import DepartmentService,UserService
from models import DepartmentCreateModel


department_service = DepartmentService()
user_service = UserService()
hospital_service = HospitalService()
class DepartmentController:
    async def create_department(self, department_details: DepartmentCreateModel, email):
        try:
            user = await user_service.get_user_by_email(email)
            if not user:
                raise UserNotFound()

            hospital = await hospital_service.get_hospital_by_email(email)         

            if not hospital:
                raise HospitalNotFound()

            existing_department = await department_service.get_departments_by_name_and_hospital_id(department_details.name, hospital.id)
            
            if existing_department:
                # raise DepartmentAlreadyExists()
                return {"success": False, "message": "Department already exists", "data": existing_department}
            department =await department_service.create_department(department_details.dict(), hospital)

            return {"success":True, "message": "Department created successfully", "data": department}
        
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    
    async def get_department_by_id(self, department_id: str, email):

        try:
            user = await user_service.get_user_by_email(email)
            if not user:
                raise UserNotFound()

            hospital = await hospital_service.get_hospital_by_email(email)
            if not hospital:
                raise HospitalNotFound()

            department = await department_service.get_departments_by_id(department_id)
            if not department:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
            return {"success":True, "message": "Department found successfully", "data": department}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def add_staff_to_department(self, department_id: str, staff_details: dict, email):
        try:
            user = await user_service.get_user_by_email(email)
            if not user:
                raise UserNotFound()
            hospital = await hospital_service.get_hospital_by_email(email)
            if not hospital:
                raise HospitalNotFound()
            department = await department_service.get_department_by_hospital_id_and_department_id(hospital_id=hospital.id, department_id=department_id)
            
            if not department:
                #   raise DepartmentNotFound()
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message": "Department not found",
                "error_code": "department_not_found",
            })
            
            user_exists_in_department = await department_service.get_user_by_email_in_department(department_id=department_id, email=staff_details["email"])
            if user_exists_in_department:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "message": "User already exists in department",
                "error_code": "user_already_exists_in_department",
            })  

            staff = await department_service.add_staff_to_department(department=department, hospital=hospital,staff_details=staff_details)

            return {"success":True, "message": "Staff added to department successfully", "data": staff}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def get_departments(self, email: str):
        try:    
            hospital = await hospital_service.get_hospital_by_email(email)
            if not hospital:
                raise HospitalNotFound()
            departments = await department_service.get_departments(hospital_id=hospital.id)
            if not departments:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No departments found")
            return {"success":True, "message": "Departments fetched successfully", "data": departments}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def delete_department(self, department_id: str, email: str):
        try:
            user = await user_service.get_user_by_email(email)
            if not user:
                raise UserNotFound()
            hospital = await hospital_service.get_hospital_by_email(email)
            if not hospital:
                raise HospitalNotFound()
            department = await department_service.get_department_by_hospital_id_and_department_id(hospital_id=hospital.id, department_id=department_id) 
            if not department:
                raise DepartmentNotFound()
            await department_service.delete_department(department=department)
            return {"success":True, "message": "Department deleted successfully"}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            
    async def delete_staff_from_department(self, department_id: str, staff_id: str, email: str):
        try:
            user = await user_service.get_user_by_email(email)
            if not user:
                raise UserNotFound()
            hospital = await hospital_service.get_hospital_by_email(email)
            if not hospital:
                raise HospitalNotFound()
            department = await department_service.get_department_by_hospital_id_and_department_id(hospital_id=hospital.id, department_id=department_id)
            if not department:
                raise DepartmentNotFound()
            staff = await user_service.get_user_by_id(staff_id)
            if not staff:
                raise UserNotFound()
            await department_service.delete_staff_from_department(department=department, staff=staff)
            return {"success":True, "message": f"Staff deleted from the {department.name} department successfully"}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))   
            
    