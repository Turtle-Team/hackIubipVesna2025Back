from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from .. import crud
from ..schemas.product import *
from ..schemas import auth
from .. import security
from ..utils.database import get_db, Session

router = APIRouter()


@router.post("/", response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    # Check if product with same market and item_id already exists
    existing_product = crud.get_product_by_market_and_item_id(
        db, product.market, product.item_id
    )
    if existing_product:
        return existing_product
    return crud.create_product(db, product.dict())


@router.get("/", response_model=List[Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/market/{market}/item/{item_id}", response_model=Product)
def read_product_by_market_and_item_id(
    market: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    db_product = crud.get_product_by_market_and_item_id(db, market, item_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    db_product = crud.update_product(db, product_id, product.dict(exclude_unset=True))
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: auth.UserAuth = Depends(security.get_current_user)
):
    if not crud.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return None 