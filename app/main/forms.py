from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import Required, Email, EqualTo
from wtforms import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from ..models import User

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you', validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    title = StringField('Pitch title', validators=[Required()])
    pitch = TextAreaField('Pitch', validators=[Required()])
    submit = SubmitField('Submit')