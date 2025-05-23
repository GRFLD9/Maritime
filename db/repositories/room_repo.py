from sqlalchemy.orm import joinedload
from db.database import create_session
from models.rooms import Room
from db.repositories.booking_repo import BookingRepository


class RoomRepository:
    @staticmethod
    def get_all_rooms():
        with create_session() as session:
            return session.query(Room).options(joinedload(Room.images)).all()

    @staticmethod
    def get_room_by_id(room_id):
        with create_session() as session:
            return session.query(Room).options(joinedload(Room.images)).get(room_id)

    @staticmethod
    def get_available_rooms(check_in, check_out):
        with create_session() as session:
            booked_room_ids = BookingRepository.get_booked_room_ids(check_in, check_out)
            query = session.query(Room).options(joinedload(Room.images))
            if booked_room_ids:
                query = query.filter(~Room.id.in_(booked_room_ids))
            return query.all()

    @staticmethod
    def create_room(room_data):
        with create_session() as session:
            room = Room(**room_data)
            session.add(room)
            session.commit()
            return room

    @staticmethod
    def delete_room(room_id):
        with create_session() as session:
            room = session.get(Room, room_id)
            if room:
                session.delete(room)
                session.commit()
