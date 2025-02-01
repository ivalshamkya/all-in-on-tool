from fastapi import File, UploadFile, HTTPException, APIRouter, Request

from helpers.format_response import format_response_success
from middlewares.limiter import limiter
from services.image_service import (compress_image)

route = APIRouter()

@route.post("/compress")
@limiter.limit("15/hour")
async def compress_image_endpoint(request: Request, file: UploadFile = File(...), quality: int = 50):
    try:
        return format_response_success(
            data=str(compress_image(file, quality)))
    except HTTPException as exc:
        raise HTTPException(500, exc)