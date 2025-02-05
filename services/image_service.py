from PIL import Image
from fastapi import File, UploadFile, HTTPException, BackgroundTasks
from helpers import image_helper as ih, s3_helper as s3
from data.responses.upload_response import UploadResponse


def compress_image(file: UploadFile = File(...), quality: int = 50, background_tasks: BackgroundTasks = None):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        image_helper = ih.ImageHelper()
        s3_helper = s3.S3Helper()

        # Process image
        image = Image.open(file.file)
        compressed_bytes = image_helper.compress_image(image, quality)


        # Generate filename and upload
        filename = image_helper.generate_filename()
        download_url = s3_helper.upload_file(
            compressed_bytes,
            filename,
            file.content_type
        )

        return download_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))