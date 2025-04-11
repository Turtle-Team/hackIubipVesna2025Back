from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .. import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Связь с пользователями
    users = relationship("User", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role(name='{self.name}', id='{self.id}')>"
