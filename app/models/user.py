from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str
    hashed_password: str
