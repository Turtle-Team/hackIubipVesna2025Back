from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Optional, Type

from database.schemas.product import Product

__all__ = ["get_products",
           "create_product",
           "update_product",
           "delete_product",
           "get_product",
           "get_product_by_market_and_item_id",
           "get_products_by_monitored_product_and_time_range"]

def create_product(db: Session, product_data: dict):
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_market_and_item_id(db: Session, market: int, item_id: int):
    return db.query(Product).filter(
        Product.market == market,
        Product.item_id == item_id
    ).first()


def update_product(db: Session, product_id: int, product_data: dict):
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


def get_products_by_monitored_product_and_time_range(
    db: Session,
    monitored_product_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> list[Type[Product]]:
    query = db.query(Product).filter(
        Product.monitored_product_id == monitored_product_id
    )
    
    if start_time:
        query = query.filter(Product.created_at >= start_time)
    if end_time:
        query = query.filter(Product.created_at <= end_time)
    
    return query.order_by(Product.created_at.desc()).offset(skip).limit(limit).all() 