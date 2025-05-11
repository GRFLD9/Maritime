from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from db.database import SqlAlchemyBase


class HikingRoute(SqlAlchemyBase):
    """Модель маршрута для активного отдыха"""

    __tablename__ = 'hiking_routes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    difficulty = Column(String(30))
    distance_km = Column(Float)
    duration_hours = Column(Float)
    location = Column(String(200))

    favorited_by = relationship("User", secondary="user_favorite_routes", back_populates="favorite_routes")