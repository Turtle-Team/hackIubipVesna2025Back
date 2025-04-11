from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    market: int = 0
    item_id: int = 0
    name: str = ''
    url: str = ''
    price: float = 0
    rating: float = 0.0
    review_count: int = 0
    buy_count: int = 0
    picture: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    market: Optional[int] = None
    item_id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    buy_count: Optional[int] = None
    picture: Optional[str] = None


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 