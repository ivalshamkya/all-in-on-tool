from models.base_model import BaseModel


class UploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    download_url: str

class ErrorResponse(BaseModel):
    detail: str