"""Functions to send mails."""
from django.core.mail import send_mail

from .models import User


def send_mail_to_user(user: User, code: str) -> None:
    """Send mail to user."""
    send_mail(
        subject='Код подтверждения',
        message=f'Код: {code}',
        from_email='from@example.com',
        recipient_list=[f'{user.email}'],
        fail_silently=False,
    )
