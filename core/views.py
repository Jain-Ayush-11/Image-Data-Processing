from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.exceptions import CSVRequestNotFoundException
from core.serializers import CSVUploadSerializer, OutputCSVRequestSerializer, OutputCSVResponseSerializer
from core.services import CSVOutputService, CSVUploadService


class UploadCSVView(APIView):
    request_serializer = CSVUploadSerializer

    def post(self, request):
        try:
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

        except Exception as e:
            # TODO: Replace print with log statement
            msg = f"Fatal Error Occurred in getting request output :: {e}"
            print(msg)
            return Response(
                {
                    'status': 'error',
                    'message': 'Unexpected Error Occurred',
                    'payload': ''
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OutputCSVView(APIView):
    request_serializer = OutputCSVRequestSerializer
    response_serializer = OutputCSVResponseSerializer
    
    def get(self, request):
        try:
            serializer = self.request_serializer(data=request.query_params)

            if not serializer.is_valid():
                return Response(
                    {
                        'status': 'error',
                        'message': serializer.errors,
                        'payload': ''
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            
            request_id = serializer.validated_data.get('request_id')

            csv_request = CSVOutputService.get_request_output(request_id=request_id)

            serializer = self.response_serializer(csv_request, context={'request': request})

            return Response(
                {
                    'status': 'success',
                    'message': '',
                    'payload': serializer.data
                }
            )
    
        except CSVRequestNotFoundException:
            return Response(
                {
                    'status': 'error',
                    'message': 'Invalid Request ID',
                    'payload': ''
                }, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            # TODO: Replace print with log statement
            msg = f"Fatal Error Occurred in getting request output :: {e}"
            print(msg)
            return Response(
                {
                    'status': 'error',
                    'message': 'Unexpected Error Occurred',
                    'payload': ''
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )