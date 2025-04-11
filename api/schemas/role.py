from pydantic import BaseModel

class RoleGet(BaseModel):
    id: int = None
    name: str

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RoleUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True
