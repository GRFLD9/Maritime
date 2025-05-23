from db.repositories.booking_repo import BookingRepository
from db.repositories.room_repo import RoomRepository
from db.repositories.user_repo import UserRepository
from exceptions import ValidationError, UserNotFoundError


class BookingService:
    @staticmethod
    def validate_booking_data(data: dict) -> None:
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        user_id = data.get("user_id")
        room_id = data.get("room_id")

        if not check_in or not check_out:
            raise ValidationError("Необходимо указать даты заезда и выезда")

        if check_in >= check_out:
            raise ValidationError("Дата выезда должна быть позже даты заезда")

        if not UserRepository.get_by_id(user_id):
            raise UserNotFoundError(f"Пользователь {user_id} не найден")

        if not RoomRepository.get_room_by_id(room_id):
            raise ValidationError(f"Комната {room_id} не найдена")

    @staticmethod
    def get_booking_by_id(booking_id: int):
        booking = BookingRepository.get_booking_by_id(booking_id)
        if not booking:
            raise ValidationError(f"Бронирование {booking_id} не найдено")
        return booking

    @staticmethod
    def get_user_bookings(user_id: int):
        return BookingRepository.get_user_bookings(user_id)

    @staticmethod
    def create_booking(data: dict):
        BookingService.validate_booking_data(data)

        user_id = data.get("user_id")
        if user_id:
            user = UserRepository.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(f"Пользователь {user_id} не найден")
        else:
            data["user_id"] = None

        return BookingRepository.create_booking_entry(data)

    @staticmethod
    def delete_booking(user_id: int, booking_id: int) -> bool:
        if not BookingRepository.delete_booking_by_user(user_id, booking_id):
            raise ValidationError(f"Бронирование {booking_id} не найдено или нет доступа")
        return True
