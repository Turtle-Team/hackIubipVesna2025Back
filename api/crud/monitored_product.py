from sqlalchemy.orm import Session

from database.schemas.monitored_product import MonitoredProduct

__all__ = ["get_all_monitored_products",
           "get_monitored_products",
           "get_monitored_product",
           "update_monitored_product",
           "delete_monitored_product",
           "create_monitored_product"]


def create_monitored_product(db: Session, user_id: int, product_data: dict):
    db_product = MonitoredProduct(user_id=user_id, **product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


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
