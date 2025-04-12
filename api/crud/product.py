from sqlalchemy.orm import Session

from database.schemas.product import Product

__all__ = ["get_products",
           "create_product",
           "update_product",
           "delete_product",
           "get_product",
           "get_product_by_market_and_item_id"]

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