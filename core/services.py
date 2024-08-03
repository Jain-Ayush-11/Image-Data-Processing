import os
from typing import List
import uuid
from django.core.files.uploadedfile import UploadedFile
from core.enums import RequestStatus
from core.models import CSVRequest, Product, Image
import pandas as pd
import requests
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.base import ContentFile

class CSVUploadService:
    @classmethod
    def create_request_with_file(cls, file: UploadedFile) -> CSVRequest:
        """
        Create a new Request object with the uploaded file.
        :param file: The uploaded CSV file for a request
        :return: The created Request object.
        """
        directory = 'media/csv_files/input/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        request_obj = CSVRequest.objects.create(input_file=file)
        return request_obj


class CSVProcessService:
    @classmethod
    def _process_input_csv(cls, request: CSVRequest) -> List[dict]:
        """
        Processes the input csv and returns the data for output csv

        :param request: CSV Request object to be processed
        :return: Output Data List for the output csv
        """
        # Read the CSV file
        df = pd.read_csv(request.input_file.path)
        
        # output data for the output csv to be generated
        output_data = []

        for idx, row in df.iterrows():
            serial_number = row['S. No.']
            name = row['Product Name']
            image_urls = row['Input Image Urls'].split(',')
            
            # Create or update the product
            product, _ = Product.objects.get_or_create(
                serial_number=serial_number,
                name=name,
                request=request
            )
            
            # Process and save each image
            output_image_urls = []
            for image_url in image_urls:
                image_url = image_url.strip()
                processed_image_url = cls._process_image(image_url)
                output_image_urls.append(processed_image_url)
                
                Image.objects.create(
                    product=product,
                    input_url=image_url,
                    output_url=processed_image_url
                )
            
            # Collect data for the output CSV
            output_data.append({
                'S. No.': serial_number,
                'Product Name': name,
                'Input Image Urls': ','.join(image_urls),
                'Output Image Urls': ','.join(output_image_urls)
            })
        
        return output_data
    
    @classmethod
    def _process_image(cls, url: str) -> str:
        """
        Processes an image by downloading it and compressing by 50%

        :param url: URL of the image to be compressed
        :return: URL of resulting compressed image
        """
        response = requests.get(url)
        image = PILImage.open(BytesIO(response.content))
        
        # Compress image by 50%
        output_image = BytesIO()
        image.save(output_image, format=image.format, quality=50)
        output_image.seek(0)
        
        # Save the compressed image
        output_image_url = cls._save_image(output_image)
        
        return output_image_url

    @classmethod
    def _save_image(cls, image_file: BytesIO) -> str:
        """
        Saves an image in the directory

        :param image_file: Image to be saved in the directory
        :return: Path of the saved Image
        """
        directory = 'media/compressed_images'
        
        # create the directory, if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # create a random filename for the compressed output image
        filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'wb') as f:
            f.write(image_file.getvalue())
        
        return f"/{file_path}"
    
    @classmethod
    def _save_output_csv(cls, output_data: list, input_csv_path: str) -> ContentFile:
        """
        Creates a CSV with the data specified

        :param output_data: List of dictionaries with the relevant data for the output CSV
        :param input_csv_path: Path of the input csv processed
        :return: Path of the resulting output csv generated
        """
        directory = 'media/csv_files/output/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        output_csv_content = pd.DataFrame(output_data).to_csv(index=False)
        output_csv_file = ContentFile(output_csv_content)
        output_csv_file.name = input_csv_path.split('/')[-1].replace('.csv', '_output.csv')
        return output_csv_file

    @classmethod
    def process_request(cls, request: CSVRequest) -> bool:
        """
        Processes the request by compressing the input url images and saving it to a new CSV file

        :param request: CSV Request object to be processed
        """
        try:
            # List for output data to create output csv
            output_data = cls._process_input_csv(request=request)
            
            # Save the output CSV
            output_csv_file = cls._save_output_csv(output_data, request.input_file.path)
            
            # Update the request output file and status
            request.output_file.save(output_csv_file.name, output_csv_file)
            request.status = RequestStatus.SUCCESS
            request.save()

            # remove the output csv from the machine
            if os.path.exists(output_csv_file.name):
                os.remove(output_csv_file.name)

            return True
        
        except Exception as e:
            # TODO: Add a log statement for the error
            print(e)

            # Mark the request as FAILED, will be picked by a reconciliation worker
            request.status = RequestStatus.FAILED
            request.save()

            return False
