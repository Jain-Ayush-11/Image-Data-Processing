from django.db.models import TextChoices


class RequestStatus(TextChoices):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
