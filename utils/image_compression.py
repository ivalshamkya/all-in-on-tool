import io
from PIL import Image

def image_compression(image: Image.Image, quality: int = 50) -> bytes:
    if image.format == "PNG":
        image = image.convert("RGB")

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    return buffer.getvalue()