from typing import List

from fastapi import APIRouter, Depends, HTTPException

from .. import crud
from .. import security
from ..schemas import auth
from ..schemas.user import *
from ..utils.database import get_db, Session

router = APIRouter()

@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db),
                current_user: auth.UserAuth = Depends(security.get_current_user)):
    return crud.create_user(db=db, login=user.login, password=user.password, role_id=user.role_id)


@router.get("/", response_model=List[UserGet])
def get_users(db: Session = Depends(get_db), current_user: auth.UserAuth = Depends(security.get_current_user)):
    return crud.get_users(db)

@router.get("/{user_id}", response_model=UserGet)
def get_user(user_id: int, db: Session = Depends(get_db),
             current_user: auth.UserAuth = Depends(security.get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Эндпоинт для получения информации о текущем пользователе
@router.get("/user/me", response_model=UserGet)
def get_user_info(db: Session = Depends(get_db),
                  current_user: auth.UserAuth = Depends(security.get_current_user)):
    db_user = crud.get_user(db, user_id=current_user.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserCreate)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db),
                current_user: auth.UserAuth = Depends(security.get_current_user)):
    return crud.update_user(db=db, user_id=user_id, login=user.login, role_id=user.role_id)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user: auth.UserAuth = Depends(security.get_current_user)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
