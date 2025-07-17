import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class LoginForm(FlaskForm):
    login_identifier = StringField(
        'Email или телефон',
        validators=[DataRequired()],
        render_kw={"placeholder": "example@mail.com или +79991234567"}
    )
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Login')

    def validate_login_identifier(self, field):
        value = field.data.strip()

        if '@' in value:
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value):
                raise ValidationError('Некорректный email')
        else:
            digits = re.sub(r'[^\d]', '', value)
            if not (7 <= len(digits) <= 15):
                raise ValidationError('Телефон должен содержать 7-15 цифр')
