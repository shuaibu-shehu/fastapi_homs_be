from pydantic import BaseModel


class HospitalOnboardModel(BaseModel):
    name: str
    address: str
    city: str
    state: str
    country: str
    contact_number: str
    contact_person: str
    email: str
