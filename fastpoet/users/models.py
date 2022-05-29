"""Models for users."""
import datetime

from sqlalchemy import (Boolean, Column, Integer, String, DateTime, Text,
                        UniqueConstraint, ForeignKey)
from sqlalchemy.orm import relationship

from fastpoet.settings.database import Base


class Role(Base):  # модель ролей, по ней создается таблица всех ролей
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)


class UserRoles(Base):  # модель соединяющая Роли и Пользователя
    __tablename__ = "user_roles"
    user_id = Column(
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        ForeignKey("roles.id"),
        primary_key=True,
        nullable=False,
    )
    role = relationship("Role")
    user = relationship("User", back_populates="roles", uselist=False)

    __table_args__ = (
        UniqueConstraint("role_id", "user_id", name="unique_user_id"),
    )


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=True) # поле можно не указывть
    first_name = Column(String, index=True)  # Имя
    last_name = Column(String, index=True)  # фамилия
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # время создания пользователя
    born_year = Column(Integer, index=True, nullable=True)
    hashed_password = Column(String) # 
    active = Column(Boolean, default=False)
    posts = relationship(  # связь с моделью юзер постс,
                           # каскадное удаление проверить в тестах
        "Post", cascade="all, delete-orphan", back_populates="author"
    )
    roles = relationship(  # связь с моделью юзер ролес, недоступно множество
        "UserRoles", back_populates="user", uselist=False
    )

    __table_args__ = (  # два поля не могут иметь одно и то же значение
        UniqueConstraint("username", "first_name", name="unique_username"),
    )

    # под вопросом, может пригодиться при проерке
    @property
    def is_active(self):
        return self.active
