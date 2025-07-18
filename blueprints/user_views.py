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

        try:
            data = {
                "email": form.email.data,
                "phone": form.phone.data,
                "password": form.password.data,
                "surname": form.surname.data,
                "name": form.name.data,
                "birth_date": form.birth_date.data,
                "city_from": form.city_from.data,
                "role": "user",
                "is_verified": False,
            }
            user = UserService.create_user(data)
            flash("Регистрация прошла успешно", "success")
            return redirect('/auth/login')
        except Exception as e:
            flash(str(e), "danger")

    return render_template("auth/register.html", form=form)


@user_blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.login_identifier.data
        password = form.password.data

        try:
            user = UserService.authenticate_user(identifier, password)
            login_user(user, remember=form.remember_me.data)
            flash("Успешный вход", "success")
            return redirect("/")

        except Exception as e:
            flash(str(e), "danger")

    return render_template("auth/login.html", form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "info")
    return redirect('/auth/login')


@user_blueprint.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@user_blueprint.route('/admin')
@role_required('admin')
def admin_dashboard():
    return render_template("admin_dashboard.html")
