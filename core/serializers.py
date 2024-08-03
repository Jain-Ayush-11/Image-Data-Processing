from rest_framework import serializers
import pandas as pd

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError('Invalid file format. Please upload a CSV file.')
        
        # Check CSV columns
        try:
            df = pd.read_csv(value)
            
            # Validate required columns
            required_columns = {'S. No.', 'Product Name', 'Input Image Urls'}
            if not required_columns.issubset(df.columns):
                raise serializers.ValidationError('CSV file is missing required columns: {}'.format(', '.join(required_columns - set(df.columns))))
        except Exception as e:
            raise serializers.ValidationError(f'Error reading CSV file: {str(e)}')
        
        return value
