from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_notification(message: str, subject: str, emails: list[str]) -> None:
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=True,
        html_message=message,
    )
