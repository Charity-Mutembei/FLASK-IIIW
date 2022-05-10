from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, SelectField
from wtforms.validators import Required, Email, EqualTo
from wtforms import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from ..models import User

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you', validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    category = SelectField('Add pitch category',choices = [('Pick-up Lines','Pick-up Lines'),('Sales','Sales'),('Innovation','Innovation'),('Humanity','Humanity'),('Music','Music'),('Tech','Tech')]) 
    name = TextAreaField('username')
    title = TextAreaField('title')
    context = TextAreaField('Pitch itself')
    submit = SubmitField('Submit')