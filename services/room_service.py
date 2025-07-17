from datetime import datetime
from db.repositories.room_repo import RoomRepository
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
    def get_available_rooms(check_in, check_out, guests=None):
        if not check_in or not check_out:
            return RoomRepository.get_all_rooms()

        if isinstance(check_in, str):
            check_in = datetime.strptime(check_in, "%d.%m.%Y").date()
        if isinstance(check_out, str):
            check_out = datetime.strptime(check_out, "%d.%m.%Y").date()

        if check_in >= check_out:
            raise ValidationError("Дата выезда должна быть позже даты заезда")

        if guests is not None:
            try:
                guests = int(guests)
                if guests <= 0:
                    raise ValueError()
            except ValueError:
                raise ValidationError("Количество гостей должно быть положительным числом")

        return RoomRepository.get_available_rooms(check_in, check_out, guests)

    @staticmethod
    def create_room(data: dict):
        required_fields = ["name", "description", "price_per_night", "capacity", "room_type"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(f"Поле '{field}' обязательно для заполнения")

        if data.get("capacity") <= 0:
            raise ValidationError("Вместимость должна быть положительным числом")

        if data.get("price_per_night") <= 0:
            raise ValidationError("Цена должна быть положительным числом")

        room = RoomRepository.create_room(data)
        return room
