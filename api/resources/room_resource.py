from flask_restful import Resource

from api.parsers.room_parser import room_filter_parser, create_room_parser
from exceptions import ValidationError
from services.room_service import RoomService


class RoomListResource(Resource):
    def get(self):
        try:
            args = room_filter_parser.parse_args()
            check_in = args.get("check_in")
            check_out = args.get("check_out")
            guests = args.get("guests")

            rooms = RoomService.get_available_rooms(check_in, check_out, guests)

            result = []
            for room in rooms:
                primary_image = next((img for img in room.images if img.is_primary), None)
                image_url = primary_image.image_url if primary_image else "/static/images/default-room.jpg"
                result.append({
                    "id": room.id,
                    "name": room.name,
                    "description": room.description[:100] + "..." if len(room.description) > 100 else room.description,
                    "capacity": room.capacity,
                    "price": room.price_per_night,
                    "image_url": image_url
                })

            return {"rooms": result}, 200

        except ValidationError as e:
            return {"error": str(e)}, 400

    def post(self):
        try:
            args = create_room_parser.parse_args()
            room = RoomService.create_room(args)
            return room, 201
        except ValidationError as e:
            return {"error": str(e)}, 400


class RoomDetailResource(Resource):
    def get(self, room_id):
        try:
            room = RoomService.get_room_by_id(room_id)
            return room.to_dict(), 200
        except ValidationError as e:
            return {"error": str(e)}, 400
