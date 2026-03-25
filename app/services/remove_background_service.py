import os
import logging
from rembg import remove
from PIL import Image
from app.utils.file_storage_utils import generate_unique_filename, get_output_filepath

logger = logging.getLogger(__name__)

async def process_remove_background(input_filepath: str, original_filename: str) -> str:
    """
    Removes the background from the image at input_filepath.
    Saves the output as a transparent PNG in the output directory.
    Returns the final filename.
    """
    try:
        # Determine output filename and path
        output_filename = generate_unique_filename(original_filename, prefix="removed-bg-", extension=".png")
        output_filepath = get_output_filepath(output_filename)

        # Process with rembg
        # We process using PIL Image for better compatibility
        input_image = Image.open(input_filepath)
        
        # remove background
        output_image = remove(input_image)
        
        # Save output image as PNG
        output_image.save(output_filepath, format="PNG")
        
        return output_filename
    except Exception as e:
        logger.error(f"Error removing background: {str(e)}")
        raise e
