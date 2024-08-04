from django.conf import settings
from rest_framework import serializers
import pandas as pd

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        if not file.name.endswith('.csv'):
            raise serializers.ValidationError('Invalid file format. Please upload a CSV file.')
        
        # Check CSV columns
        try:
            df = pd.read_csv(file)
            
            # Validate required columns
            required_columns = {'S. No.', 'Product Name', 'Input Image Urls'}
            if not required_columns.issubset(df.columns):
                raise serializers.ValidationError('CSV file is missing required columns: {}'.format(', '.join(required_columns - set(df.columns))))

            return file
    
        except Exception as e:
            raise serializers.ValidationError(f'Error reading CSV file: {str(e)}')


class OutputCSVRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()


class OutputCSVResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    output_file_url = serializers.SerializerMethodField(required=False)

    def get_output_file_url(self, instance):
        request = self.context.get('request')
        if not request:
            return f'{settings.BASE_URL}{instance.output_file.url}'
        # build the absolute uri for the path
        return request.build_absolute_uri(instance.output_file.url)


class WebhookPayloadSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(source='id')
    output_csv = serializers.SerializerMethodField()

    def get_output_csv(self, instance):
        return OutputCSVResponseSerializer(instance, context=self.context).data
