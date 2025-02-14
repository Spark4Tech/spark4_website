# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import Contact
from app.email.email_service import (
    send_contact_confirmation_email,
    send_contact_notification_email
)
from app.forms import ContactForm
from app import db
import logging

main = Blueprint('main', __name__)

logger = logging.getLogger(__name__)

@main.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@main.route('/')
def index():
    form = ContactForm()
    return render_template('index.html', form=form)

@main.route('/teach')
def teach():
    form = ContactForm()
    return render_template('teach.html', form=form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form submission with validation."""
    form = ContactForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Create new contact record
                contact = Contact(
                    name=form.name.data,
                    email=form.email.data,
                    message=form.message.data
                )
                
                # Save to database
                db.session.add(contact)
                db.session.commit()
                
                # Send emails
                send_contact_confirmation_email(contact.email, contact.name)
                send_contact_notification_email(contact)
                
                flash('Thank you for your interest! We\'ll be in touch soon.', 'success')
                return redirect(url_for('main.index'))
                
            except Exception as e:
                logger.error(f"Error processing contact form: {str(e)}", exc_info=True)
                db.session.rollback()
                flash('Something went wrong. Please try again later.', 'error')
        
        # If form validation failed, flash the first error
        else:
            for field, errors in form.errors.items():
                flash(f"{errors[0]}", 'error')
                break
    
    # For GET requests or failed validation, return to the form
    return redirect(url_for('main.index', _anchor='contact'))

@main.route('/signup', methods=['POST'])
def signup():
    # Handle newsletter signup form submission
    email = request.form.get('email')

    # Logic to store the email in your database or mailing list
    # TODO: Implement email storage

    flash('Thank you for subscribing!', 'success')
    return redirect(url_for('main.index'))

@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@main.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')