from rembg import remove, new_session
from PIL import Image, ImageFilter, ImageEnhance
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageProcessor:
    @staticmethod
    async def remove_background(image_data: bytes) -> bytes:
        try:
            logger.info("Starting background removal process")

            # Load image without scaling
            input_image = Image.open(io.BytesIO(image_data)).convert("RGBA")

            # Optionally enhance contrast
            enhancer = ImageEnhance.Contrast(input_image)
            input_image = enhancer.enhance(1.1)

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            input_image.save(img_byte_arr, format='PNG')
            enhanced_image_data = img_byte_arr.getvalue()

            # Create session with adjusted parameters
            session = new_session(
                "isnet-general-use",
                providers=['cpu'],
                parameters={
                    "alpha_matting": True,
                    "alpha_matting_foreground_threshold": 240,
                    "alpha_matting_background_threshold": 10,
                    "alpha_matting_erode_size": 0,
                    "alpha_matting_base_size": 2048,
                }
            )

            # Remove background
            output_data = remove(
                enhanced_image_data,
                session=session,
                post_process_mask=True,
                only_mask=False
            )

            logger.info("Background removal completed")

            # Post-process the output
            output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")

            # Obtain mask
            mask_data = remove(
                enhanced_image_data,
                session=session,
                post_process_mask=True,
                only_mask=True
            )
            mask_image = Image.open(io.BytesIO(mask_data)).convert("L")

            # Optional: Enhance mask using Unsharp Mask
            mask_image_enhanced = mask_image.filter(
                ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
            )

            # Apply the enhanced mask to the output image
            output_image.putalpha(mask_image_enhanced)

            # Optional: Sharpen the output image
            output_image = output_image.filter(ImageFilter.SHARPEN)

            # Save the final image
            final_byte_arr = io.BytesIO()
            output_image.save(
                final_byte_arr,
                format='PNG',
                quality=100,
                optimize=False,
                dpi=(300, 300)
            )

            return final_byte_arr.getvalue()

        except Exception as e:
            logger.error(f"Error in background removal: {str(e)}")
            raise Exception(f"Failed to process image: {str(e)}")