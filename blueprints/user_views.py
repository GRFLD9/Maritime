from flask import Blueprint, render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user

from db.database import create_session
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from models.users import User
from services.user_service import UserService
from utils.decorators import role_required  # добавим позже

user_blueprint = Blueprint('user_views', __name__)


@user_blueprint.route('/')
@user_blueprint.route('/main')
def main():
    return render_template('main.html')


@user_blueprint.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают", "danger")
            return render_template("register.html", form=form)

        try:
            data = {
                "email": form.email.data,
                "phone": form.phone.data,
                "password_hash": form.password.data,
                "surname": form.surname.data,
                "name": form.name.data,
                "birth_date": form.birth_date.data,
                "city_from": form.city_from.data,
                "role": "user",
                "is_verified": False,
            }
            user = UserService.register_user(data)
            flash("Регистрация прошла успешно", "success")
            return redirect('/login')
        except Exception as e:
            flash(str(e), "danger")

    return render_template("register.html", form=form)


@user_blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.login_identifier.data
        password = form.password.data

        try:
            user_dict = UserService.authenticate_user(identifier, password)
            with create_session() as session:
                user_obj = session.get(User, user_dict["id"])

            if user_obj:
                login_user(user_obj, remember=form.remember_me.data)
                flash("Успешный вход", "success")
                return redirect("/")
            else:
                flash("Ошибка при загрузке пользователя", "danger")

        except Exception as e:
            flash(str(e), "danger")

    return render_template("login.html", form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect('/login')


@user_blueprint.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@user_blueprint.route('/admin')
@role_required('admin')  # Только для админа
def admin_dashboard():
    return render_template("admin_dashboard.html")


@user_blueprint.route('/rooms')
def rooms():
    return render_template('rooms.html', active_page='rooms')
