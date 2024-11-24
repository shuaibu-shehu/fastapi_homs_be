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

