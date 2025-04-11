from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import setting
from database import Session
from .schemas.auth import UserAuth

SECRET_KEY = setting.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 6000


# Функция для получения сессии базы данных
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функция для верификации JWT токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Функция для получения текущего пользователя из JWT
def get_current_user(token: str):
    payload = verify_token(token)
    return UserAuth(**payload)
