from fastapi import APIRouter, Depends
from typing import Optional
from lib.role_checker import RoleChecker
from lib.dependencies import AccessTokenBearer
from controllers import DepartmentController
from models import DepartmentCreateModel, StaffCreateModel, DailyOxygenConsumptionModel

router = APIRouter()

access_token_bearer= AccessTokenBearer()
department_controller = DepartmentController()
role_cherker = RoleChecker(["doctor","admin"])
@router.get("/")
async def get_departments(token_details= Depends(access_token_bearer)):
    return await department_controller.get_departments(token_details["email"])

@router.post("/")
async def create_department(department_details: DepartmentCreateModel, token_details= Depends(access_token_bearer)):
     return await department_controller.create_department(department_details, token_details["email"]) 
 
@router.get("/{department_id}")
async def get_department(department_id: str, token_details= Depends(access_token_bearer)):
     return await department_controller.get_department_by_id(department_id, token_details["email"])

@router.post("/staffs/{department_id}")
async def add_staff_to_department(department_id: str, staff_details: StaffCreateModel, token_details= Depends(access_token_bearer)):
     print(staff_details.model_dump())
     return await department_controller.add_staff_to_department(department_id, staff_details.model_dump(), token_details["email"])

@router.delete("/{department_id}")
async def delete_department(department_id: str, token_details= Depends(access_token_bearer)):
     return await department_controller.delete_department(department_id, token_details["email"])

@router.delete("/staffs/{department_id}/{staff_id}")
async def delete_staff_from_department(department_id: str, staff_id: str, token_details= Depends(access_token_bearer)):
     return await department_controller.delete_staff_from_department(department_id, staff_id, token_details["email"])

# @router.post("/daily-oxygen-entry/{department_id}/{staff_id}")
# async def record_daily_oxygen_entry(department_id: str, staff_id: str,oxygen_entry: DailyOxygenConsumptionModel, token_details= Depends(access_token_bearer)):
#      return await department_controller.record_daily_oxygen_entry(department_id, staff_id, oxygen_entry, token_details["email"])


# @router.get("/daily-oxygen-entries/{department_id}")
# async def get_daily_oxygen_entries(department_id: str, token_details= Depends(access_token_bearer)):
#      return await department_controller.get_daily_oxygen_entries(department_id, token_details["email"])  

  