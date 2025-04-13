from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .. import Base

class NotificationSettings(Base):
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    email = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)
    
    user = relationship("User", back_populates="notification_settings")
