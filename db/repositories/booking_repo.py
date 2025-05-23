from sqlalchemy.orm import joinedload

from db.database import create_session
from models import Room
from models.booking import Booking


class BookingRepository:
    @staticmethod
    def get_booking_by_id(booking_id):
        with create_session() as session:
            return session.get(Booking, booking_id)

    @staticmethod
    def delete_booking_by_user(user_id, booking_id):
        with create_session() as session:
            booking = session.query(Booking).filter_by(id=booking_id, user_id=user_id).first()
            if booking:
                session.delete(booking)
                session.commit()
                return True
            return False

    @staticmethod
    def get_available_rooms(check_in, check_out):
        with create_session() as session:
            booked_room_ids = BookingRepository.get_booked_room_ids(check_in, check_out)
            query = session.query(Room).options(joinedload(Room.images))
            if booked_room_ids:
                query = query.filter(~Room.id.in_(booked_room_ids))
            return query.all()

    @staticmethod
    def create_booking_entry(data):
        with create_session() as session:
            booking = Booking(
                user_id=data.get("user_id"),
                room_id=data["room_id"],
                check_in=data["check_in"],
                check_out=data["check_out"],
                notes=data.get("notes", ""),
                status=data.get("status", "pending"),

                guests=data.get("guests"),

                guest_name=data.get("guest_name"),
                guest_phone=data.get("guest_phone"),
                guest_email=data.get("guest_email"),
            )
            session.add(booking)
            session.commit()
            session.refresh(booking)
            return booking

    @staticmethod
    def get_booked_room_ids(check_in, check_out):
        with create_session() as session:
            bookings = session.query(Booking).filter(
                Booking.check_in < check_out,
                Booking.check_out > check_in
            ).all()

            return [b.room_id for b in bookings]

    @staticmethod
    def get_user_bookings(user_id: int):
        with create_session() as session:
            return (
                session.query(Booking)
                .options(joinedload(Booking.room))
                .filter(Booking.user_id == user_id)
                .all()
            )
