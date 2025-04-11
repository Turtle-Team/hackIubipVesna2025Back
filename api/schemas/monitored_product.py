from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MonitoredProductBase(BaseModel):
    name: str
    url: Optional[str] = None


class MonitoredProductCreate(MonitoredProductBase):
    pass


class MonitoredProductUpdate(MonitoredProductBase):
    name: Optional[str] = None
    url: Optional[str] = None


class MonitoredProduct(MonitoredProductBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 