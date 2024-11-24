from fastapi import HTTPException, status
from lib import error_logger
from lib.errors import HospitalNotFound
from models import HospitalOnboardModel

from config.connection import db

class HospitalService():
    async def onboard(self, hospital_details: dict):        
        return await db.prisma.hospital.create(data=hospital_details)

    async def get_hospital_by_email(self, email):
        return await db.prisma.hospital.find_unique(where={"email": email})
    
    # async def user_exists_in_hospital(self, email):
    #     return await db.prisma.hospital.find_unique(where={"email": email}, include={"users": True})
    async def verify_hospital(self, token_data):
             try:
                hospital = await self.get_hospital_by_email(token_data["email"])
                if not hospital:
                    raise HospitalNotFound()
                await db.prisma.hospital.update(
                    where={
                        "id": hospital.id
                    },
                    data={
                        "verified": True
                    }
                )

                await db.prisma.verificationtoken.delete(
                    where={
                        "token": token_data["token"]
                    }
                )
     
                return {"success":True, "message": "email verified successfully"}
             except Exception as e:
                  error_logger.error(e)
                  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            
    async def get_hospital_by_id(self, hospital_id: str):
        return await db.prisma.hospital.find_unique(where={"id": hospital_id}, include={"departments": True})

    async def get_departments(self, hospital_id: str):
        return await db.prisma.department.find_many(where={"hospital_id": hospital_id})
   
    async def get_users(self, hospital_id: str):
        return await db.prisma.user.find_many(where={"hospitalId": hospital_id})

 