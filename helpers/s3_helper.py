import boto3
from botocore.exceptions import ClientError
from config import get_settings
from fastapi import HTTPException

class S3Helper:
    def __init__(self):
        settings = get_settings()
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_BUCKET_NAME

    def upload_file(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        try:
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_bytes,
                ContentType=content_type
            )
            return self.generate_presigned_url(filename)
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

    def generate_presigned_url(self, filename: str) -> str:
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': filename
                },
                ExpiresIn=3600
            )
            return url
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))