from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

def send_registration_email(user):
    """
    Send an email to the user after successful registration with both HTML and plain text.
    """
    subject = "Welcome! Complete your registration"
    
    # Create the plain text version of the message
    text_content = f"""
    Dear {user.get_full_name()},

    You have been successfully registered on our platform.
    Here are your login credentials:

    Email: {user.email}
    Temporary Password: {user.passport_id}

    Please log in using these credentials and change your password to complete your registration.

    Best regards,
    Your Company
    """

    # Create the HTML version of the message (this can be more styled)
    html_content = render_to_string('registration_email_template.html', {
        'user': user,
        'email': user.email,
        'password': user.passport_id
    })
    
    # Create the email object
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    
    # Attach the HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send the email
    email.send(fail_silently=False)