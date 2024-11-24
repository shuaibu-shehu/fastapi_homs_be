
from fastapi import Depends, status , HTTPException
from lib.error_logger import error_logger
from lib.errors import HospitalAlreadyExists
from services import HospitalService,AuthService
from models import HospitalOnboardModel
from config.config import Config

from jinja2 import Environment, FileSystemLoader

auth_service = AuthService()
hospital_service = HospitalService()\


template_env = Environment(loader=FileSystemLoader(searchpath=Config.TEMPLATE_FOLDER))

email_template = template_env.get_template("verify_email_hospital_onboarding.html")

class HospitalController:

    async def onboard(self,hospital_details: dict):
            data= hospital_details.dict()
            existing_hospital = await hospital_service.get_hospital_by_email(data["email"]) 
            if existing_hospital: 
                raise HospitalAlreadyExists()  
                              
            hospital = await  hospital_service.onboard(data)

            subject = "Email Verification"
                
            await auth_service.send_email_verification(hospital,email_template,subject, is_email_verification=True)
                
            return { "message": "Email has been sent to verify hospital account", "data": hospital}
  
    async def verify(self, token_data):
        try:             
            return  await  hospital_service.verify_hospital(token_data)            

        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ooops! Something went wrong")

    async def get_hospital(self, hospital_id: str, email: str):
        try:           
            hospital = await hospital_service.get_hospital_by_id(hospital_id)
            if not hospital:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
            return {"success":True, "message": "Hospital fetched successfully", "data": hospital}
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_departments(self, hospital_id: str):
        try:
            hospital = await hospital_service.get_hospital_by_id(hospital_id)
            if not hospital:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
            return await hospital_service.get_departments(hospital_id)
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def get_users(self, hospital_id: str, email: str):
        try:
            hospital = await hospital_service.get_hospital_by_id(hospital_id)
            if not hospital:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
            return await hospital_service.get_users(hospital_id)
        except Exception as e:
            error_logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


 