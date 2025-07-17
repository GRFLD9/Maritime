from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin

from db.database import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель пользователя"""

    __tablename__ = 'users'

    SERIALIZE_RULES = (
        '-password_hash',
        '-favorite_routes',
        '-bookings',
        '-created_at',
        '-updated_at',
        '-favorite_routes.favorited_by'
    )

    @classmethod
    def get_serialize_rules(cls):
        return cls.SERIALIZE_RULES

    @property
    def full_name(self):
        return f"{self.name} {self.surname}".strip()

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    birth_date = Column(Date, nullable=True)
    city_from = Column(String, nullable=True)

    created_at = Column(DateTime, default=func.datetime('now', 'localtime'))
    updated_at = Column(DateTime, onupdate=func.datetime('now', 'localtime'))
    is_verified = Column(Boolean, default=False)
    role = Column(String, default='guest')

    bookings = relationship("Booking", back_populates="user")
    favorite_routes = relationship("HikingRoute", secondary="user_favorite_routes", back_populates="favorited_by")
