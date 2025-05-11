from sqlalchemy import Table, Column, Integer, ForeignKey

from db.database import SqlAlchemyBase

user_favorite_routes = Table(
    'user_favorite_routes',
    SqlAlchemyBase.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('route_id', Integer, ForeignKey('hiking_routes.id'), primary_key=True)
)

from .users import User
from .rooms import Room
from .booking import Booking
from .hiking_routes import HikingRoute
from .room_images import RoomImage

__all__ = ['User', 'Room', 'Booking', 'HikingRoute', 'RoomImage', user_favorite_routes]
