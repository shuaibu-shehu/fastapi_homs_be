from typing import Optional
from fastapi import APIRouter, Depends

from lib.dependencies import AccessTokenBearer
from controllers import BedController
from models import UserLoginModel, BedCreateModel
from fastapi import status

router = APIRouter()

bed_controller = BedController()
access_token_bearer = AccessTokenBearer()

@router.post("/{department_id}")
async def create_bed(department_id: str, bed_details:dict, token_details= Depends(access_token_bearer)):
    return await bed_controller.create_bed(department_id, bed_details, token_details["email"])
 

@router.get("/{department_id}")
async def get_beds(department_id: str):
    return await bed_controller.get_beds(department_id)

# @router.get("/daily-consumption/{bed_id}")
# async def get_daily_consumptions(bed_id: str, start_date: str, end_date: str):
#     print("start_date", start_date)
#     print("end_date", end_date)
#     return await bed_controller.get_daily_consumptions(bed_id, start_date, end_date)


@router.delete("/{bed_id}")
async def delete_bed(bed_id: str):
    return await bed_controller.delete_bed(bed_id)

@router.get("/{bed_id}/sensor")
async def get_sensor_data(bed_id: str, date: str):
 
    return await bed_controller.get_sensor_data(bed_id, date)


@router.get("/{bed_id}/daily-consumption")
async def get_daily_consumptions_by_bed_id(bed_id: str):
    return await bed_controller.get_daily_consumptions_by_bed_id(bed_id)


@router.get("/{department_id}/today/{date}")
async def get_daily_consumptions_by_department_id(department_id: str, date: Optional[str] = None):
    return await bed_controller.get_daily_consumptions_by_department_id(department_id, date)

@router.get("/total-consumption/{department_id}")
async def get_total_consumption_by_department_id(department_id: str):
    return await bed_controller.get_total_consumption_by_department_id(department_id)
