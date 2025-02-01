import io
import os
import tempfile

from PIL import Image
from fastapi import File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse

from utils.image_compression import image_compression


def compress_image(file: UploadFile = File(...), quality: int = 50, background_tasks: BackgroundTasks = None):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    image = Image.open(file.file)
    compressed_image = image_compression(image, quality)

    # # Save the compressed image to a temporary file
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
    #     temp_file.write(compressed_image)
    #     temp_file_path = temp_file.name
    #
    # # Add a background task to delete the temporary file after serving
    # if background_tasks:
    #     background_tasks.add_task(os.remove, temp_file_path)

        # Return the temporary file as a response
    return compressed_image

    # return StreamingResponse(compressed_image, media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=compressed.jpg"})
