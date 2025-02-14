# email_service/email_service.py

from postmarker.core import PostmarkClient
from config import Config
from typing import Optional
from flask import url_for, current_app, render_template
from app.models import Contact
import logging

postmark_api_key = Config.POSTMARK_API_KEY
postmark_sender_email = Config.POSTMARK_SENDER_EMAIL
postmark_notify_email = Config.POSTMARK_NOTIFY_EMAIL

postmark = PostmarkClient(postmark_api_key)

# Set up logger
logger = logging.getLogger(__name__)

def send_contact_confirmation_email(to: str, name: str) -> Optional[dict]:
    """Send confirmation email to user who submitted contact form."""
    logger.info(f"Sending contact confirmation email to {to}")
    subject = "Thanks for your interest in Wellness Corner!"
    body = render_template(
        'emails/contact_confirmation.html',
        name=name
    )
    return send_email(to, subject, body)

def send_contact_notification_email(contact: Contact) -> Optional[dict]:
    """Send notification email to admin about new contact submission."""
    logger.info(f"Sending contact notification email for {contact.email}")
    subject = "New Wellness Corner Early Access Request"
    body = render_template(
        'emails/contact_notification.html',
        contact=contact
    )
    return send_email(
        postmark_notify_email,  # Send to admin email
        subject,
        body
    )

def send_email(to, subject, html_body):
    logger.info(f"Attempting to send email to {to} with subject: {subject}")
    try:
        response = postmark.emails.send(
            From=postmark_sender_email,
            To=to,
            Subject=subject,
            HtmlBody=html_body
        )
        logger.info(f"Email sent successfully to {to}. Message ID: {response['MessageID']}")
        return response
    except Exception as e:
        logger.error(f"Error sending email to {to}: {str(e)}", exc_info=True)
        return None

def send_token_email(to, token):
    logger.info(f"Preparing to send token email to {to}")
    subject = f"{token} is your Wellness Corner login code"
    body = render_template('emails/token_email.html', token=token)
    result = send_email(to, subject, body)
    if result:
        logger.info(f"Token email sent successfully to {to}")
    else:
        logger.warning(f"Failed to send token email to {to}")
    return result

def send_connection_request_email(to, coach_name, invitation_token):
    logger.info(f"Preparing to send connection request email from {coach_name} to {to}")
    subject = f"Connection Request from {coach_name} on Wellness Corner"
    
    try:
        with current_app.app_context():
            accept_url = url_for('main.accept_invitation', token=invitation_token, _external=True)
        logger.debug(f"Generated accept_url: {accept_url}")
    except Exception as e:
        logger.error(f"Error generating accept_url: {str(e)}", exc_info=True)
        return None
    
    coach_first_name, coach_last_name = coach_name.split(' ', 1) if ' ' in coach_name else (coach_name, '')
    
    body = render_template('emails/connection_request.html', 
                           coach_first_name=coach_first_name,
                           coach_last_name=coach_last_name,
                           accept_url=accept_url)
    result = send_email(to, subject, body)
    if result:
        logger.info(f"Connection request email sent successfully from {coach_name} to {to}")
    else:
        logger.warning(f"Failed to send connection request email from {coach_name} to {to}")
    return result

def send_invitation_email(to, coach_name, coach_id):
    logger.info(f"Preparing to send invitation email from {coach_name} to {to}")
    subject = f"Invitation to join Wellness Corner from {coach_name}"
    try:
        with current_app.app_context():
            join_url = url_for('main.register', invited_by=coach_id, _external=True)
        logger.debug(f"Generated join_url: {join_url}")
    except Exception as e:
        logger.error(f"Error generating join_url: {str(e)}", exc_info=True)
        return None
    
    body = render_template('emails/invitation.html', coach_name=coach_name, join_url=join_url)
    result = send_email(to, subject, body)
    if result:
        logger.info(f"Invitation email sent successfully from {coach_name} to {to}")
    else:
        logger.warning(f"Failed to send invitation email from {coach_name} to {to}")
    return result