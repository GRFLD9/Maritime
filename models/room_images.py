from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class RoomImage(SqlAlchemyBase, SerializerMixin):
    """Модель для хранения фотографий номеров"""

    __tablename__ = 'room_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)

    room = relationship("Room", back_populates="images")
    serialize_rules = ('-room',)