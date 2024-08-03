from django.db import models
import uuid

from core.enums import RequestStatus

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CSVRequest(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    input_file = models.FileField(upload_to='csv_files/input/')
    output_file = models.FileField(upload_to='csv_files/output/', null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )


class Product(BaseModel):
    serial_number = models.IntegerField()
    name = models.CharField(max_length=255)
    request = models.ForeignKey(CSVRequest, related_name='products', on_delete=models.CASCADE)


class Image(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    input_url = models.URLField()
    output_url = models.URLField(null=True, blank=True)
