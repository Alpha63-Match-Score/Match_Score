from fastapi import UploadFile, HTTPException
import boto3
import os
from datetime import datetime
import uuid
from PIL import Image
import io

from src.core.config import settings


class S3Service:
    MAX_SIZE = (300, 300)
    ALLOWED_FORMATS = {'.jpg', '.jpeg', '.png'}
    JPEG_QUALITY = 90
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

    def __init__(self):
        self.bucket_name = settings.AWS_BUCKET_NAME
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )

    def validate_image(self, file: UploadFile) -> None:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in self.ALLOWED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. "
                       f"Allowed formats: {', '.join(self.ALLOWED_FORMATS)}"
            )

        # Check file size
        file.file.seek(0, 2)  # end of the file
        size = file.file.tell()  # current position
        file.file.seek(0)  # return to the beginning

        if size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. "
                       f"Maximum size is {self.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

    def process_image(self, image_data: bytes) -> bytes:
        try:
            image = Image.open(io.BytesIO(image_data))

            # Convert to RGB if needed
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')

            # Resize if needed
            if image.size[0] > self.MAX_SIZE[0] or image.size[1] > self.MAX_SIZE[1]:
                image.thumbnail(self.MAX_SIZE, Image.Resampling.LANCZOS)

            # Optimize and convert to bytes
            output = io.BytesIO()
            image.save(
                output,
                format='JPEG',
                quality=self.JPEG_QUALITY,
                optimize=True
            )
            return output.getvalue()

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing image: {str(e)}"
            )

    def upload_file(self, file: UploadFile, folder: str) -> str:
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            extension = os.path.splitext(file.filename)[1]
            new_filename = f"{folder}/{timestamp}_{unique_id}{extension}"

            # Read file content
            contents = file.file.read()

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=new_filename,
                Body=contents,
                ContentType=file.content_type
            )

            # Generate URL
            return f"https://{self.bucket_name}.s3.amazonaws.com/{new_filename}"

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error uploading file: {str(e)}"
            )
        finally:
            file.file.close()

    def delete_file(self, file_url: str) -> bool:
        try:
            if not file_url:
                return True

            # Extract key from URL
            key = file_url.split('.com/')[1]

            # Delete from S3
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

s3_service = S3Service()