from api.parsers.booking_parser import create_booking_parser
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from exceptions import ValidationError
from services.booking_service import BookingService


class BookingResource(Resource):
    @jwt_required()
    def get(self, booking_id):
        """Получить бронирование по ID (только своё)"""
        user_id = get_jwt_identity()
        booking = BookingService.get_booking_by_id(booking_id)

        if not booking or booking.user_id != user_id:
            return {"error": "Бронирование не найдено или доступ запрещён"}, 404

        return booking.to_dict(), 200

    @jwt_required()
    def delete(self, booking_id):
        """Удалить бронирование (только своё)"""
        user_id = get_jwt_identity()
        try:
            deleted = BookingService.delete_booking(user_id, booking_id)
            if deleted:
                return "", 204
            else:
                return {"error": "Бронирование не найдено или доступ запрещён"}, 404
        except Exception as e:
            return {"error": str(e)}, 400


class BookingListResource(Resource):
    @jwt_required()
    def get(self):
        """Получить все бронирования текущего пользователя"""
        user_id = get_jwt_identity()
        bookings = BookingService.get_user_bookings(user_id)
        return [b.to_dict() for b in bookings], 200

    @jwt_required()
    def post(self):
        """Создать бронирование"""
        args = create_booking_parser.parse_args()
        user_id = get_jwt_identity()

        try:
            booking_data = {
                "user_id": user_id,
                "room_id": args["room_id"],
                "check_in": args["check_in"],
                "check_out": args["check_out"],
                "notes": args.get("notes", ""),
                "status": "pending",
            }
            new_booking = BookingService.create_booking(booking_data)
            return new_booking.to_dict(), 201
        except ValidationError as e:
            return {"error": str(e)}, 400
