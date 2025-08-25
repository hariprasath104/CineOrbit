# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User, UserRole  # Import UserRole

class RegisterForm(FlaskForm):
    """User registration form."""
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    
    # NEW: Add a role selection dropdown
    role = SelectField(
        'Register as a',
        choices=[(role.name, role.value.capitalize()) for role in UserRole],
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

    def validate_username(self, username):
        """Validate that the username is not already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')