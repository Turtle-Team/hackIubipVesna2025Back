from typing import List

from fastapi import APIRouter, Depends, HTTPException

from .. import crud
from ..schemas.role import *
from ..schemas import auth
from .. import security
from ..utils.database import get_db, Session

router = APIRouter()

# Эндпоинт для создания роли
@router.post("/", response_model=RoleCreate)
def create_role(role: RoleCreate, db: Session = Depends(get_db), current_user: auth.UserAuth = Depends(security.get_current_user)):
    return crud.create_role(db=db, name=role.name)


# Эндпоинт для получения всех ролей
@router.get("/", response_model=List[RoleGet])
def get_roles(db: Session = Depends(get_db), current_user: auth.UserAuth = Depends(security.get_current_user)):
    return crud.get_roles(db)


# Эндпоинт для получения роли по ID
@router.get("/{role_id}", response_model=RoleCreate)
def get_role(role_id: int, db: Session = Depends(get_db), current_user: auth.UserAuth = Depends(security.get_current_user)):
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


# Эндпоинт для обновления роли
@router.put("/{role_id}", response_model=RoleCreate)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db), current_user: auth.UserAuth = Depends(security.get_current_user)):
    db_role = crud.update_role(db=db, role_id=role_id, name=role.name)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


# Эндпоинт для удаления роли
@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: auth.UserAuth = Depends(security.get_current_user)):
    db_role = crud.delete_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}
