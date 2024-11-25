from typing import Optional
from pydantic import BaseModel


class DepartmentCreateModel(BaseModel):
    name: str
    status: Optional[bool] = None


class StaffCreateModel(BaseModel):
    name: str
    contact: str
    role: str
    email: str
    status: str



class DailyOxygenConsumptionModel(BaseModel):
    oxygen_consumption: float
    bed_number: int
    is_first_time_usage: bool
    remarks: Optional[str] = None

