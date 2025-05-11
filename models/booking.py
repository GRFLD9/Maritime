from sqlalchemy import Column, Integer, Date, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.database import SqlAlchemyBase


class Booking(SqlAlchemyBase):
    """Модель бронирования номера"""

    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    status = Column(String(20), default='pending')
    total_price = Column(Float)
    notes = Column(String(300))

    user = relationship("User", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")