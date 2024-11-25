from fastapi import HTTPException, status
from lib.mail import create_message, mail
from lib.utils import generate_password_hash, generate_random_string
from lib.error_logger import error_logger
from models import DepartmentCreateModel
from config.connection import db

class DepartmentService:
    async def create_department(self, department_details: dict, hospital):
        try: 
            print("reached here", department_details["name"], hospital)
            return await db.prisma.department.create(
                data={
                    "name": department_details["name"],
                    "status": department_details["status"],
                    "hospital": {"connect": {"id": hospital.id}}
                    
                }
            )
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        # print(department_details)
        # pass
    
    async def get_departments_by_name_and_hospital_id(self, name: str, hospital_id: str):
        try:
            return await db.prisma.department.find_many(
                where={
                    "name": name,
                    "hospitalId": hospital_id
                }
            )    
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def get_department_by_id(self, department_id: str):
        try:
            return await db.prisma.department.find_unique(
                where={
                    "id": department_id
                }
            )    
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

    async def get_department_by_hospital_id_and_department_id(self, hospital_id: str, department_id: str):
        try:
            return await db.prisma.department.find_unique(where={"hospitalId": hospital_id, "id": department_id})
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def add_staff_to_department(self, department:dict, hospital: dict, staff_details: dict):
        try:
            password = generate_random_string(6)
            hashed_password = generate_password_hash(password)
            user = await db.prisma.user.create(
                data={
                    **staff_details,
                    "verified": True,
                    "password": hashed_password,
                    "department": {"connect": {"id": department.id}},
                    "hospital": {"connect": {"id": hospital.id}}
                }
            )
            subject = "Welcome to the department of " + department.name 
            body = f"Use the following login details to access your account: \n email: {user.email} \n password: {password}"
            message =  create_message(recipients=[user.email], subject=subject, body=body) 
            await mail.send_message(message)
            return user
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    async def get_user_by_email_in_department(self, department_id: str, email: str):
        return await db.prisma.user.find_first(where={"departmentId": department_id, "email": email})

    async def get_departments(self, hospital_id: str):
        return await db.prisma.department.find_many(where={"hospitalId": hospital_id}, include={"users": True})

    async def delete_department(self, department: dict):
        return await db.prisma.department.delete(where={"id": department.id})

    async def delete_staff_from_department(self, department: dict, staff: dict):
        return await db.prisma.user.delete(where={"id": staff.id})
        
    