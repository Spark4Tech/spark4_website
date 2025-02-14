# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import re

class ContactForm(FlaskForm):
    """Form for early access registration."""
    name = StringField('Name', validators=[
        DataRequired(message="Please enter your name"),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Please enter your email"),
        Email(message="Please enter a valid email address"),
        Length(max=100, message="Email must be less than 100 characters")
    ])
    
    message = TextAreaField('Message', validators=[
        Length(min=0, max=1000, message="Message must be less than 1000 characters")
    ])
    
    submit = SubmitField('Get on the List!')
    
    def validate_name(self, field):
        # Check for any numbers or special characters except hyphen and apostrophe
        if re.search(r'[^a-zA-Z\s\-\']', field.data):
            raise ValidationError('Name can only contain letters, spaces, hyphens, and apostrophes')
    
    def validate_email(self, field):
        # Additional email validation if needed
        if 'temp' in field.data.lower() or 'disposable' in field.data.lower() or 'reply' in field.data.lower():
            raise ValidationError('Please use a permanent email address')