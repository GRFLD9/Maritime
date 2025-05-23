from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange, Optional, Email


class BookingForm(FlaskForm):
    check_in = DateField("Дата заезда", format="%d.%m.%Y", validators=[DataRequired()])
    check_out = DateField("Дата выезда", format="%d.%m.%Y", validators=[DataRequired()])
    guests = IntegerField("Количество гостей", validators=[DataRequired(), NumberRange(min=1)])
    notes = TextAreaField("Примечания")

    guest_name = StringField("Ваше имя", validators=[Optional()])
    guest_phone = StringField("Телефон", validators=[Optional()])
    guest_email = StringField("Email", validators=[Optional(), Email()])

    submit = SubmitField("Забронировать")

    def validate(self, **kwargs):
        return super().validate(**kwargs)
