from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import SqlAlchemyBase


class Room(SqlAlchemyBase):
    """Модель номера в базе отдыха"""

    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    amenities = Column(String(300))
    room_type = Column(String(50))
    bookings = relationship("Booking", back_populates="room")

    images = relationship("RoomImage", back_populates="room")