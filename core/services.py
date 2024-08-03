from django.core.files.uploadedfile import UploadedFile
from core.models import CSVRequest


class CSVUploadService:
    @classmethod
    def create_request_with_file(cls, file: UploadedFile) -> CSVRequest:
        """
        Create a new Request object with the uploaded file.
        :param file: The uploaded CSV file for a request
        :return: The created Request object.
        """
        request_obj = CSVRequest.objects.create(file=file)
        return request_obj

