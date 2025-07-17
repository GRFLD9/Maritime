from flask_restful import reqparse

room_filter_parser = reqparse.RequestParser()
room_filter_parser.add_argument("check_in", type=str, required=True, help="Дата заезда обязательна")
room_filter_parser.add_argument("check_out", type=str, required=True, help="Дата выезда обязательна")
room_filter_parser.add_argument("guests", type=int, default=2, help="Количество гостей")

create_room_parser = reqparse.RequestParser()
create_room_parser.add_argument("name", type=str, required=True, help="Название комнаты обязательно")
create_room_parser.add_argument("description", type=str, required=True, help="Описание обязательно")
create_room_parser.add_argument("price_per_night", type=float, required=True, help="Цена за ночь обязательна")
create_room_parser.add_argument("capacity", type=int, required=True, help="Вместимость обязательна")
create_room_parser.add_argument("amenities", type=str, required=False)
create_room_parser.add_argument("room_type", type=str, required=True, help="Тип комнаты обязателен")
