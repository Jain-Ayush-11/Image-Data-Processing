from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializers import CSVUploadSerializer
from core.services import CSVUploadService


class UploadCSVView(APIView):
    request_serializer = CSVUploadSerializer

    def post(self, request):
        serializer = self.request_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': serializer.errors,
                    'payload': ''
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        file = serializer.validated_data['file']
        
        # Create a new request with the uploaded file
        request_obj = CSVUploadService.create_request_with_file(file=file)
        
        # Return success response
        return Response(
            {
                'status': 'success',
                'message': 'File uploaded successfully',
                'payload': {'request_id': str(request_obj.id)}
            }, status=status.HTTP_201_CREATED
        )
