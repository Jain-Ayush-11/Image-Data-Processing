from django.db import models
import uuid

from core.enums import RequestStatus


class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=50,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    serial_number = models.IntegerField()
    name = models.CharField(max_length=255)
    request = models.ForeignKey(Request, related_name='products', on_delete=models.CASCADE)


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    input_url = models.URLField()
    output_url = models.URLField(null=True, blank=True)
