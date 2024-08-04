from django.db.models import TextChoices


class RequestStatusChoices(TextChoices):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
