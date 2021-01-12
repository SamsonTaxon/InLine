from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email

class EmailForm(FlaskForm):
    # email = EmailField('Email', validators=[DataRequired(), Email()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Get Nline')

class PhoneForm(FlaskForm):
	submit = SubmitField('Get NLine')