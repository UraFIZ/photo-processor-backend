from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from app.services.image_processor import ImageProcessor
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    logger.info("Starting background removal")
    try:
        image_data = await file.read()
        processor = ImageProcessor()
        result = await processor.remove_background(image_data)
        return Response(content=result, media_type="image/png")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return Response(
            content=str(e),
            status_code=500
        )