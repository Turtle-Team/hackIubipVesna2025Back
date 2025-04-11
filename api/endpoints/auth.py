from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Session
from .. import crud, security
from ..schemas.auth import *
import database.schemas.user

router = APIRouter()


# Функция для получения сессии базы данных
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# Эндпоинт для регистрации пользователя
@router.post("/register/", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли уже пользователь с таким логином
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Хешируем пароль и создаем нового пользователя
    hashed_password = database.schemas.user.User().set_password(user.password)
    db_user = crud.create_user(db=db, login=user.login, password=hashed_password, role_id=user.role_id)
    return db_user


# Эндпоинт для входа пользователя (получение JWT токена)
@router.post("/login/")
def login_for_access_token(form_data: Login, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=form_data.login)
    if db_user is None or not db_user.verify_password(form_data.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    # Генерация токена
    access_token = security.create_access_token(data={'user_id': db_user.id, 'role_id': db_user.role.id})
    return {"access_token": access_token, "token_type": "bearer"}
