from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError, InputRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), InputRequired(message="Пароль обязателен")])
    password_again = PasswordField('Repeat password', validators=[DataRequired(), InputRequired(message="Пароль обязателен")])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%d.%m.%Y', validators=[DataRequired()])
    city_from = StringField('Hometown', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_password_again(self, field):
        if field.data != self.password.data:
            raise ValidationError('Пароли не совпадают')
