from sqlalchemy.orm import Session
import asyncio
from datetime import datetime

from database.schemas.monitored_product import MonitoredProduct
from database.schemas.product import Product
from ..utils import product_fetcher, product_poller

__all__ = ["get_all_monitored_products",
           "get_monitored_products",
           "get_monitored_product",
           "update_monitored_product",
           "delete_monitored_product",
           "create_monitored_product"]


def create_monitored_product(db: Session, user_id: int, product_data: dict):
    if 'http' in product_data.get('name'):
        product_data['url'] = product_data['name']
        product_data.pop('name')

    if product_data.get("url"):
        product_info = asyncio.run(product_fetcher.fetch_product_by_url(product_data["url"]))
        
        if product_info:
            product_data["name"] = product_info["name"]
            
            db_monitored_product = MonitoredProduct(user_id=user_id, **product_data)
            db.add(db_monitored_product)
            db.commit()
            db.refresh(db_monitored_product)
            
            product_data = {
                "monitored_product_id": db_monitored_product.id,
                "market": product_info["market"],
                "item_id": product_info["item_id"],
                "name": product_info["name"],
                "url": product_info["url"],
                "price": product_info["price"],
                "rating": product_info["rating"],
                "review_count": product_info["review_count"],
                "buy_count": product_info["buy_count"],
                "picture": product_info["picture"],
                "time_ship": product_info["time_ship"],
                "datetime_ship": datetime.fromisoformat(product_info["datetime_ship"].replace("Z", "+00:00")) if product_info.get("datetime_ship") else None,
                "geo": product_info["geo"]
            }

            db_product = Product(**product_data)
            db.add(db_product)
            db.commit()
            
            return db_monitored_product

    if product_data.get("name"):
        pooler = product_poller.ProductPoller()
        product_info = asyncio.run(pooler.fetch_products(product_data["name"]))

        if product_info:
            product_data["name"] = product_info["name"]

            db_monitored_product = MonitoredProduct(user_id=user_id, **product_data)
            db.add(db_monitored_product)
            db.commit()
            db.refresh(db_monitored_product)

            product_data = {
                "monitored_product_id": db_monitored_product.id,
                "market": product_info["market"],
                "item_id": product_info["item_id"],
                "name": product_info["name"],
                "url": product_info["url"],
                "price": product_info["price"],
                "rating": product_info["rating"],
                "review_count": product_info["review_count"],
                "buy_count": product_info["buy_count"],
                "picture": product_info["picture"],
                "time_ship": product_info["time_ship"],
                "datetime_ship": datetime.fromisoformat(
                    product_info["datetime_ship"].replace("Z", "+00:00")) if product_info.get("datetime_ship") else None,
                "geo": product_info["geo"]
            }

            db_product = Product(**product_data)
            db.add(db_product)
            db.commit()

            return db_monitored_product

    db_monitored_product = MonitoredProduct(user_id=user_id, **product_data)
    db.add(db_monitored_product)
    db.commit()
    db.refresh(db_monitored_product)
    return db_monitored_product


def get_monitored_products(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(MonitoredProduct).filter(
        MonitoredProduct.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_all_monitored_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MonitoredProduct).offset(skip).limit(limit).all()


def get_monitored_product(db: Session, product_id: int, user_id: int):
    return db.query(MonitoredProduct).filter(
        MonitoredProduct.id == product_id,
        MonitoredProduct.user_id == user_id
    ).first()


def update_monitored_product(db: Session, product_id: int, user_id: int, product_data: dict):
    db_product = get_monitored_product(db, product_id, user_id)
    if db_product:
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_monitored_product(db: Session, product_id: int, user_id: int):
    db_product = get_monitored_product(db, product_id, user_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
