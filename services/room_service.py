from db.repositories.room_repo import RoomRepository
from db.repositories.booking_repo import BookingRepository
from exceptions import ValidationError


class RoomService:
    @staticmethod
    def get_all_rooms():
        return RoomRepository.get_all_rooms()

    @staticmethod
    def get_room_by_id(room_id: int):
        room = RoomRepository.get_room_by_id(room_id)
        if not room:
            raise ValidationError(f"Комната с ID {room_id} не найдена")
        return room

    @staticmethod
    def get_available_rooms(check_in, check_out):
        return RoomRepository.get_available_rooms(check_in, check_out)
