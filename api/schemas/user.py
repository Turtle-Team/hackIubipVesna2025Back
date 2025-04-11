import typing
from typing import Optional

from pydantic import BaseModel



class UserCreate(BaseModel):
    user_id: typing.Optional[int]
    login: str
    role_id: typing.Optional[int]
    password: str

    class Config:
        orm_mode = True


class Role(BaseModel):
    id: int
    name: str

class UserGet(BaseModel):
    login: str
    id: int
    role: Role

