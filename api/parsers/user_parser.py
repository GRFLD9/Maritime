from flask_restful import reqparse
from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d.%m.%Y').date()
    except ValueError:
        raise ValueError("Неверный формат даты. Используйте ДД.ММ.ГГГГ")

create_parser = reqparse.RequestParser()
create_parser.add_argument('email', required=True, type=str, help='Email обязателен')
create_parser.add_argument('phone', required=True, type=str, help='Телефон обязателен')
create_parser.add_argument('password', required=True, type=str, help='Пароль обязателен')  # изменено
create_parser.add_argument('name', required=True, type=str, help='Имя обязательно')
create_parser.add_argument('surname', required=True, type=str, help='Фамилия обязательна')
create_parser.add_argument('birth_date', type=parse_date, required=True, help='Дата рождения обязательна (ДД.ММ.ГГГГ)')
create_parser.add_argument('city_from', type=str, required=True, help='Родной город обязателен')
create_parser.add_argument('is_verified', type=bool, required=False, default=False)
create_parser.add_argument('role', type=str, required=False, default='guest')

update_parser = reqparse.RequestParser()
update_parser.add_argument('email', type=str, required=False)
update_parser.add_argument('phone', type=str, required=False)
update_parser.add_argument('name', type=str, required=False)
update_parser.add_argument('surname', type=str, required=False)
update_parser.add_argument('birth_date', type=parse_date, required=False)
update_parser.add_argument('city_from', type=str, required=False)
update_parser.add_argument('is_verified', type=bool, required=False)
update_parser.add_argument('role', type=str, required=False)
