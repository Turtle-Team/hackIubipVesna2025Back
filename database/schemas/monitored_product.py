from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .. import Base

class MonitoredProduct(Base):
    __tablename__ = 'monitored_products'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String(2048), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="monitored_products")
    products = relationship("Product", back_populates="monitored_product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MonitoredProduct(name='{self.name}', user_id='{self.user_id}')>" 