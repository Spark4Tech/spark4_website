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

@main.route('/service-details/<service_id>')
def service_details(service_id):
    """
    Returns HTML content for service details via HTMX request
    """
    # TODO: Replace with actual service data retrieval logic
    services = {
        'digital-presence': {
            'title': 'Digital Presence Services',
            'description': 'We help you build a compelling online presence that attracts and engages your target audience.',
            'services': [
                {
                    'name': 'Website Development',
                    'description': 'Custom-designed, responsive websites optimized for performance, payments and conversion.'
                },
                {
                    'name': 'SEO Optimization',
                    'description': 'Best practice optimizations to improve your visibility in search engines and drive organic traffic.'
                },
                {
                    'name': 'Content Strategy',
                    'description': 'Tailored content planning and distribution methods that resonates with your audience and supports your business goals.'
                }
            ]
        },
        'custom-applications': {
            'title': 'Custom Application Services',
            'description': 'We build tailored software solutions that address your unique business challenges.',
            'services': [
                {
                    'name': 'Web Applications',
                    'description': 'Secure full-stack web applications with intuitive interfaces and integrations.'
                },
                {
                    'name': 'API Development',
                    'description': 'Custom APIs that connect your systems and enable seamless data exchange.'
                },
                {
                    'name': 'AI Integration',
                    'description': 'Implementing artificial intelligence capabilities to enhance your applications and automate processes.'
                }
            ]
        },
        'business-operations': {
            'title': 'Business Operations Services',
            'description': 'We optimize your workflows and systems to improve efficiency and drive growth.',
            'services': [
                {
                    'name': 'Process Automation',
                    'description': 'Streamline repetitive tasks and workflows to reduce manual effort and minimize errors.'
                },
                {
                    'name': 'Data Analytics',
                    'description': 'Transform your data into actionable insights with dashboards and reporting tools.'
                },
                {
                    'name': 'Digital Transformation Strategy',
                    'description': 'Comprehensive roadmaps for leveraging technology to achieve your business objectives.'
                }
            ]
        }
    }
    
    # Get service details or return error if service_id is invalid
    service = services.get(service_id)
    if not service:
        return "Service not found", 404
    
    # Render template with service details
    return render_template('partials/service_details.html', service=service)

@main.route('/empty')
def empty():
    """Return an empty response for closing content"""
    return ""

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
                
                # For HTMX requests, return both updates
                if "HX-Request" in request.headers:
                    return f"""
                        <div id="contact-heading">
                            <h2 class="text-4xl font-bold mb-12 text-center text-white">Ready to Ignite Your Digital Future?</h2>
                            <p class="text-4xl font-bold mb-12 text-center text-white">Let's Go!</p>
                        </div>
                        <div id="contact-form" class="max-w-xl mx-auto text-center">
                            <p class="text-xl text-gray-300">Thanks for reaching out! We'll be in touch soon.</p>
                        </div>
                    """, 200, {
                        "HX-Trigger": "showSuccessToast"
                    }
                
                # For regular requests, use flash and redirect
                flash('Thank you for your interest! We\'ll be in touch soon.', 'success')
                return redirect(url_for('main.index'))
                
            except Exception as e:
                logger.error(f"Error processing contact form: {str(e)}", exc_info=True)
                db.session.rollback()

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

@main.route('/stash-it')
def stash_it():
    return render_template('stash_it.html')

@main.route('/stash-it-privacy-policy')
def stash_it_privacy_policy():
    return render_template('stash_it_privacy_policy.html')