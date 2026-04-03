import logging
from PIL import Image, ImageOps
from app.utils.file_storage_utils import generate_unique_filename, get_output_filepath

logger = logging.getLogger(__name__)

# Pixel dimensions at ~150 DPI — high enough for print quality
PAS_PHOTO_SIZES = {
    "2x3": (236, 354),
    "3x4": (354, 472),
    "4x6": (472, 709),
}

BACKGROUND_COLORS = {
    "red":  (206, 17, 38),
    "blue": (0, 70, 160),
}


async def process_pas_photo(
    input_filepath: str,
    original_filename: str,
    size_key: str,
    bg_color_key: str,
) -> str:
    """
    Generates a passport-style photo (pas foto):
      1. Remove background (rembg)
      2. Composite subject onto a solid background color
      3. Fit / center subject in the chosen canvas size
      4. Save as high-quality JPEG

    Returns the output filename.
    """
    if size_key not in PAS_PHOTO_SIZES:
        raise ValueError(f"Ukuran tidak valid: {size_key}. Pilihan: {list(PAS_PHOTO_SIZES.keys())}")
    if bg_color_key not in BACKGROUND_COLORS:
        raise ValueError(f"Warna background tidak valid: {bg_color_key}. Pilihan: {list(BACKGROUND_COLORS.keys())}")

    target_w, target_h = PAS_PHOTO_SIZES[size_key]
    bg_rgb = BACKGROUND_COLORS[bg_color_key]

    try:
        # --- 1. Remove background (rembg) --------------------
        try:
            from rembg import remove as rembg_remove
            src = Image.open(input_filepath).convert("RGBA")
            subject_rgba = rembg_remove(src)
        except Exception as rembg_err:
            logger.warning(f"rembg gagal ({rembg_err}), menggunakan foto asli sebagai fallback.")
            subject_rgba = Image.open(input_filepath).convert("RGBA")

        # --- 2. Create solid background canvas -------------------
        canvas = Image.new("RGB", (target_w, target_h), bg_rgb)

        # --- 3. Fit & center subject (preserve aspect ratio) -----
        # Scale subject so it fills ~90% of the canvas height (leaving small top/bottom padding)
        pad_ratio = 0.90
        max_subject_h = int(target_h * pad_ratio)
        max_subject_w = int(target_w * pad_ratio)

        subject_rgba = _fit_image(subject_rgba, max_subject_w, max_subject_h)

        # Center paste
        paste_x = (target_w - subject_rgba.width) // 2
        paste_y = (target_h - subject_rgba.height) // 2

        # Split alpha for transparency paste
        canvas.paste(subject_rgba.convert("RGB"), (paste_x, paste_y), mask=subject_rgba.split()[3])

        # --- 4. Save output as JPEG (print quality) ---------------
        output_filename = generate_unique_filename(
            original_filename, prefix="pasfoto-", extension=".jpg"
        )
        output_filepath = get_output_filepath(output_filename)

        canvas.save(output_filepath, format="JPEG", quality=95, dpi=(150, 150))
        return output_filename

    except Exception as e:
        logger.error(f"Error generating pas photo: {e}")
        raise e


def _fit_image(img: Image.Image, max_w: int, max_h: int) -> Image.Image:
    """Scale image to fit within (max_w, max_h) while preserving aspect ratio."""
    ratio = min(max_w / img.width, max_h / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    return img.resize((new_w, new_h), Image.LANCZOS)
