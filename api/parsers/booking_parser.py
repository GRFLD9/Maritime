from flask_restful import reqparse
from datetime import date

create_booking_parser = reqparse.RequestParser()
create_booking_parser.add_argument("room_id",   type=int,       required=True,  help="room_id обязателен",         location='json')
create_booking_parser.add_argument("check_in",  type=lambda x: date.fromisoformat(x), required=True, help="Дата заезда (YYYY-MM-DD)", location='json')
create_booking_parser.add_argument("check_out", type=lambda x: date.fromisoformat(x), required=True, help="Дата выезда (YYYY-MM-DD)", location='json')
create_booking_parser.add_argument("notes",     type=str,       required=False, location='json')
create_booking_parser.add_argument("guests",    type=int,       required=True,  help="Количество гостей обязательно", location='json')

update_booking_parser = reqparse.RequestParser()
update_booking_parser.add_argument("check_in",  type=lambda x: date.fromisoformat(x), required=False, help="Дата заезда (YYYY-MM-DD)", location='json')
update_booking_parser.add_argument("check_out", type=lambda x: date.fromisoformat(x), required=False, help="Дата выезда (YYYY-MM-DD)", location='json')
update_booking_parser.add_argument("notes",     type=str,       required=False, location='json')
update_booking_parser.add_argument("guests",    type=int,       required=False, help="Количество гостей", location='json')
