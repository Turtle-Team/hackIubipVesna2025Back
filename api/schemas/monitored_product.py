from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from .product import Product


class MonitoredProductBase(BaseModel):
    product_id: int
    target_price: float


class MonitoredProductCreate(MonitoredProductBase):
    pass


class MonitoredProductUpdate(MonitoredProductBase):
    product_id: Optional[int] = None
    target_price: Optional[float] = None


class MonitoredProduct(MonitoredProductBase):
    id: int
    user_id: int
    product: Product
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 