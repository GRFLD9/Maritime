from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from api.parsers.booking_parser import create_booking_parser, update_booking_parser
from exceptions import ValidationError
from services.booking_service import BookingService


class BookingListResource(Resource):
    @jwt_required()
    def get(self):
        """Получить все бронирования текущего пользователя"""
        user_id = int(get_jwt_identity())
        bookings = BookingService.get_user_bookings(user_id)
        # bookings — список dict
        return bookings, 200

    @jwt_required()
    def post(self):
        """Создать бронирование"""
        args = create_booking_parser.parse_args()
        user_id = int(get_jwt_identity())

        try:
            booking_data = {
                "user_id": user_id,
                "room_id": args["room_id"],
                "check_in": args["check_in"],
                "check_out": args["check_out"],
                "guests": args["guests"],
                "notes": args.get("notes", ""),
                "status": "pending",
            }
            new_booking = BookingService.create_booking(booking_data)
            # new_booking — dict
            return new_booking, 201
        except ValidationError as e:
            return {"error": str(e)}, 400


class BookingResource(Resource):
    @jwt_required()
    def get(self, booking_id):
        """Получить бронирование по ID (только своё)"""
        user_id = int(get_jwt_identity())
        try:
            booking = BookingService.get_booking_by_id(booking_id)
        except ValidationError as e:
            return {"error": str(e)}, 404

        if booking["user_id"] != user_id:
            return {"error": "Доступ запрещён"}, 404

        return booking, 200

    @jwt_required()
    def put(self, booking_id):
        """Обновить своё бронирование"""
        user_id = int(get_jwt_identity())
        args = update_booking_parser.parse_args()

        try:
            updated = BookingService.update_booking(user_id, booking_id, args)
            # updated — dict
            return updated, 200
        except ValidationError as e:
            msg = str(e).lower()
            status = 404 if "не найден" in msg or "запрещ" in msg else 400
            return {"error": str(e)}, status

    @jwt_required()
    def delete(self, booking_id):
        """Удалить бронирование (только своё)"""
        user_id = int(get_jwt_identity())
        try:
            BookingService.delete_booking(user_id, booking_id)
            return "", 204
        except ValidationError as e:
            msg = str(e).lower()
            status = 404 if "не найден" in msg or "запрещ" in msg else 400
            return {"error": str(e)}, status
