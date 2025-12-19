from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email(subject, html_content, to_email, reply_to=None):
    if not settings.SENDGRID_API_KEY:
        raise Exception("SENDGRID_API_KEY no está configurada")

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    if reply_to:
        message.reply_to = reply_to

    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
