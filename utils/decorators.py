from functools import wraps

from flask import redirect, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import current_user

from exceptions import UserNotFoundError
from services.user_service import UserService


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Требуется вход в систему", "warning")
                return redirect("/login")

            if current_user.role not in roles:
                flash("У вас нет доступа к этой странице", "danger")
                return redirect("/")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def jwt_role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()

            try:
                user = UserService.get_user(user_id)
            except UserNotFoundError:
                return {"error": "Пользователь не найден"}, 404

            if user["role"] not in roles:
                return {"error": "Доступ запрещён"}, 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator
