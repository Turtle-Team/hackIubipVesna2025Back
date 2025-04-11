from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .. import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    market = Column(Integer, nullable=False, default=0)
    item_id = Column(Integer, nullable=False, default=0)
    name = Column(String(255), nullable=False, default='')
    url = Column(String(512), nullable=False, default='')
    price = Column(Float, nullable=False, default=0)
    rating = Column(Float, nullable=False, default=0.0)
    review_count = Column(Integer, nullable=False, default=0)
    buy_count = Column(Integer, nullable=False, default=0)
    picture = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    monitored_products = relationship("MonitoredProduct", back_populates="product")

    def __repr__(self):
        return f"<Product(name='{self.name}', market='{self.market}', item_id='{self.item_id}')>" 