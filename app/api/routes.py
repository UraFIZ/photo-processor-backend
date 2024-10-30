import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from app.services.image_processor import ImageProcessor

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/remove-background", name="Remove Background")
async def remove_background(
    file: UploadFile = File(..., description="Image file to remove background from")
):
    try:
        logger.info(f"Processing file: {file.filename}")
        
        # Log content type and size
        logger.info(f"Content type: {file.content_type}")
        
        # Read the file
        image_data = await file.read()
        logger.info(f"File size: {len(image_data)} bytes")
        
        # Process image
        processor = ImageProcessor()
        result = await processor.remove_background(image_data)
        
        logger.info("Background removal completed successfully")
        return Response(
            content=result,
            media_type="image/png",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
            }
        )
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add OPTIONS method handler
@router.options("/remove-background")
async def remove_background_options():
    return Response(
        content="",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )