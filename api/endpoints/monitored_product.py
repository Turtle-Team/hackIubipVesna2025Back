from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Session
from .. import crud
from ..schemas.monitored_product import *
from ..schemas import auth
from .. import security

router = APIRouter()


# Функция для получения сессии базы данных
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MonitoredProduct)
def create_product(
    product: MonitoredProductCreate,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    return crud.create_monitored_product(db, current_user.user_id, product.dict())


@router.get("/", response_model=List[MonitoredProduct])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    products = crud.get_monitored_products(db, current_user.user_id, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=MonitoredProduct)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    db_product = crud.get_monitored_product(db, product_id, current_user.user_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}", response_model=MonitoredProduct)
def update_product(
    product_id: int,
    product: MonitoredProductUpdate,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    db_product = crud.update_monitored_product(db, product_id, current_user.user_id, product.dict(exclude_unset=True))
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    if not crud.delete_monitored_product(db, product_id, current_user.user_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return None 