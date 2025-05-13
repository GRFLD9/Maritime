from datetime import date

from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash

from db.repositories.user_repo import UserRepository
from exceptions import UserNotFoundError, ValidationError


class UserService:
    @staticmethod
    def validate_user_data(data: dict, is_update: bool = False):
        """Валидация данных пользователя"""
        # Валидация телефона
        if 'phone' in data and not data['phone'].startswith('+'):
            raise ValidationError("Телефон должен начинаться с +")

        # Валидация пароля (только при создании или явном обновлении)
        if not is_update or 'password' in data:
            if len(data.get('password', '')) < 8:
                raise ValidationError("Пароль должен быть минимум 8 символов")

        # Валидация даты рождения
        if 'birth_date' in data:
            UserService._validate_birth_date(data['birth_date'])

    @staticmethod
    def _validate_birth_date(value: date) -> None:
        """Проверка возраста (18+)"""
        if not value:
            raise ValidationError("Дата рождения обязательна")

        age = relativedelta(date.today(), value).years
        if age < 18:
            raise ValidationError("Пользователь должен быть старше 18 лет")

    # CRUD методы
    @staticmethod
    def get_user(user_id: int) -> dict:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")
        return user

    @staticmethod
    def get_all_users() -> list[dict]:
        return UserRepository.get_all()

    @staticmethod
    def create_user(data: dict) -> dict:
        UserService.validate_user_data(data)
        data["password_hash"] = generate_password_hash(data.pop("password"))
        return UserRepository.create_user(data)

    @staticmethod
    def update_user(user_id: int, data: dict) -> dict:
        UserService.validate_user_data(data, is_update=True)
        user = UserRepository.update_user(user_id, data)
        if not user:
            raise UserNotFoundError(f"Пользователь {user_id} не найден")
        return user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        if not UserRepository.delete_user(user_id):
            raise UserNotFoundError(f"Пользователь {user_id} не найден")
        return True

    @staticmethod
    def register_user(data: dict) -> dict:
        UserService.validate_user_data(data)
        data["password_hash"] = generate_password_hash(data["password_hash"])
        return UserRepository.create_user(data)

    @staticmethod
    def authenticate_user(identifier: str, password: str) -> dict:
        user = UserRepository.get_by_email_or_phone(identifier)
        if not user:
            raise ValidationError("Пользователь не найден")

        if not check_password_hash(user["password_hash"], password):
            raise ValidationError("Неверный пароль")

        return user
