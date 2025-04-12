from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .. import Base

# Настройка контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(100), unique=True, nullable=False)
    password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = relationship("Role", back_populates="users")
    monitored_products = relationship("MonitoredProduct", back_populates="user", cascade="all, delete-orphan")
    notification_settings = relationship("NotificationSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(login='{self.login}', role='{self.role}', id='{self.id}'')>"

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)
        return self.password
