"""Functions to send mails."""
import random

from django.core.mail import send_mail

from .models import ConfirmationCode, User


def generate_random_code() -> int:
    """Return randomly generated number in range 1831596 to 9531389."""
    return random.randint(1831596, 9531389)


def send_mail_to_user(user: User) -> None:
    """Send mail to user."""
    code: int = generate_random_code()
    try:
        user_code: ConfirmationCode = ConfirmationCode.objects.get(user=user)
        user_code.code = code
        user_code.save()
    except ConfirmationCode.DoesNotExist:
        user_code: ConfirmationCode = ConfirmationCode.objects.create(
            user=user, code=code)
    send_mail(
        subject='Код подтверждения',
        message=f'Код: {code}',
        from_email='from@example.com',
        recipient_list=[f'{user.email}'],
        fail_silently=False,
    )


def check_code(user: User, code: int) -> bool:
    """Check confirmation code."""
    try:
        user_code = ConfirmationCode.objects.get(user=user)
    except ConfirmationCode.DoesNotExist:
        return False
    return user_code.code == code
