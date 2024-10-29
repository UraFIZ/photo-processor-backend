from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import Response  # Add this import
from app.services.image_processor import ImageProcessor

router = APIRouter()

@router.post("/remove-background")
async def remove_background(file: UploadFile):
    # Add file validation
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image file
        image_data = await file.read()
        
        # Process image
        processor = ImageProcessor()
        result = await processor.remove_background(image_data)
        
        # Return processed image
        return Response(
            content=result,
            media_type="image/png"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))