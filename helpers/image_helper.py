import random
import string

from PIL import Image
import io
from datetime import datetime
from utils import image_compression

class ImageHelper:
    @staticmethod
    def compress_image(image: Image.Image, quality: int) -> bytes:
        return image_compression.image_compression(image, quality)

    @staticmethod
    def generate_filename() -> str:
        chars = string.ascii_letters + string.digits
        size = 21
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{''.join(random.choice(chars) for _ in range(size))}{timestamp}"