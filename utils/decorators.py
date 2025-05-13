from functools import wraps

from flask import redirect, flash
from flask_login import current_user


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
