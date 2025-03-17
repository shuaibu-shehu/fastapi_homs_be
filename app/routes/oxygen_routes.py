
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from models import DailyOxygenConsumptionModel
from lib.role_checker import RoleChecker
from lib import error_logger
from lib.dependencies import AccessTokenBearer, VerificationTokenBearer
from controllers import OxygenController
from fastapi import status
router = APIRouter()


verification_token_bearer= VerificationTokenBearer()

access_token_bearer= AccessTokenBearer()

role_checker = RoleChecker(["admin"])

oxygen_controller = OxygenController()


@router.post("/{department_id}/{staff_id}")
async def record_daily_oxygen_entry(department_id: str, staff_id: str, oxygen_entry: DailyOxygenConsumptionModel, token_details= Depends(access_token_bearer)):
    print(department_id, staff_id, oxygen_entry, token_details)
    return await oxygen_controller.record_daily_oxygen_entry(department_id, staff_id, oxygen_entry.model_dump(), token_details["email"])

@router.get("/daily/entries/{department_id}")
async def get_daily_oxygen_entries(department_id: str, email: str):
    return await oxygen_controller.get_daily_oxygen_entries(department_id, email)

@router.get('/daily/{department_id}/{date}')
async def get_daily_overall_oxygen_consumption(
    department_id: str,
    date: str):
    return await oxygen_controller.get_daily_overall_oxygen_consumption(department_id, date)



@router.delete('/entry/{id}')
async def delete_daily_oxygen_entry(id: str, token_details= Depends(access_token_bearer)):
    return await oxygen_controller.delete_daily_oxygen_entry(id, token_details["email"])


@router.delete('/daily/{department_id}/{date}/{oxygen_consumption}')
async def delete_daily_overall_oxygen_consumption(department_id: str, date: str, oxygen_consumption: float):
    return await oxygen_controller.delete_daily_overall_oxygen_consumption(department_id, date, oxygen_consumption)
