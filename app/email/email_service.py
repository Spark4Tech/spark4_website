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
    subject = "Thanks for contacting Spark4!"
    body = render_template(
        'emails/contact_confirmation.html',
        name=name
    )
    return send_email(to, subject, body)

def send_contact_notification_email(contact: Contact) -> Optional[dict]:
    """Send notification email to admin about new contact submission."""
    logger.info(f"Sending contact notification email for {contact.email}")
    subject = "New Spark4 Contact Request"
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
    subject = f"{token} is your Spark4 login code"
    body = render_template('emails/token_email.html', token=token)
    result = send_email(to, subject, body)
    if result:
        logger.info(f"Token email sent successfully to {to}")
    else:
        logger.warning(f"Failed to send token email to {to}")
    return result