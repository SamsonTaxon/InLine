from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo


# class EmailForm(FlaskForm):
#     email = EmailField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Get Nline')

# class PhoneForm(FlaskForm):
# 	submit = SubmitField('Get NLine')

class PhoneForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')