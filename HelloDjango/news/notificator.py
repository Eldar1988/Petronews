from .models import Notification


def notification(host, error):
    Notification.objects.create(
        not_text=f'{host} {error}'
    )


