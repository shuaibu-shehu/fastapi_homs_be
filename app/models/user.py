from pydantic import BaseModel


class UserCreateModel(BaseModel):
    username: str
    email: str
    password: str

class UserLoginModel(BaseModel):
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str
    hashed_password: str
