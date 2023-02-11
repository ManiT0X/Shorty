from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, EqualTo


class Register(FlaskForm):
    username = StringField('', validators=[DataRequired()])
    email = EmailField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired(), length(8, 24)])
    password_verification = PasswordField('', validators=[DataRequired(), length(8, 24),
                                                          EqualTo('password', message='')])
    submit = SubmitField('Sign me up!')

