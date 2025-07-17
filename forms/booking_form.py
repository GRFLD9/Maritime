from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange, Optional, Email, ValidationError, Length
from datetime import date


class BookingForm(FlaskForm):
    check_in = DateField("Дата заезда", format="%d.%m.%Y", validators=[DataRequired(message="Укажите дату заезда")])
    check_out = DateField("Дата выезда", format="%d.%m.%Y", validators=[DataRequired(message="Укажите дату выезда")])
    guests = IntegerField("Количество гостей", validators=[
        DataRequired(message="Укажите количество гостей"),
        NumberRange(min=1, message="Минимум 1 гость")
    ])
    notes = TextAreaField("Примечания", validators=[Optional(), Length(max=1000, message="Слишком длинное примечание")])

    guest_name = StringField("Ваше имя", validators=[Optional(), Length(min=2, max=100, message="Имя должно содержать от 2 до 100 символов")])
    guest_phone = StringField("Телефон", validators=[Optional(), Length(min=5, max=30, message="Неверный формат телефона")])
    guest_email = StringField("Email", validators=[Optional(), Email(message="Введите корректный email")])

    submit = SubmitField("Забронировать")

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user

    def validate(self, **kwargs):
        is_valid = super().validate(**kwargs)
        if self.check_in.data and self.check_out.data:
            if self.check_out.data <= self.check_in.data:
                self.check_out.errors.append("Дата выезда должна быть позже даты заезда")
                is_valid = False
            if self.check_in.data < date.today():
                self.check_in.errors.append("Дата заезда не может быть в прошлом")
                is_valid = False


        if not (self.current_user and self.current_user.is_authenticated):
            if not self.guest_name.data or not self.guest_phone.data or not self.guest_email.data:
                if not self.guest_name.data:
                    self.guest_name.errors.append("Введите имя")
                if not self.guest_phone.data:
                    self.guest_phone.errors.append("Введите номер телефона")
                if not self.guest_email.data:
                    self.guest_email.errors.append("Введите email")
                is_valid = False

        return is_valid
