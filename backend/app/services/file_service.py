import os
from pdf2image import convert_from_path
from docx import Document
from PIL import Image, ImageDraw
from app.config.log_config import logger

UPLOAD_DIR = "uploads"
TEMP_IMG_DIR = os.path.join(UPLOAD_DIR, "temp_images")
os.makedirs(TEMP_IMG_DIR, exist_ok=True)


def get_file_extension(filename: str):
    """Return the lowercase file extension."""
    try:
        ext = filename.lower().split(".")[-1]
        logger.debug(f"Detected file extension: {ext}", extra={"filename": filename})
        return ext
    except Exception as e:
        logger.exception("Failed to get file extension", extra={"filename": filename})
        raise


def pdf_to_images(file_path: str):
    """
    Convert a PDF file to a list of PNG images.

    Args:
        file_path: Path to the PDF file.

    Returns:
        List of generated PNG image paths.
    """
    try:
        logger.info("Converting PDF to images", extra={"file_path": file_path})
        images = convert_from_path(file_path)
        image_paths = []

        for i, img in enumerate(images):
            path = os.path.join(TEMP_IMG_DIR, f"{os.path.basename(file_path)}_{i}.png")
            img.save(path, "PNG")
            image_paths.append(path)
            logger.debug("Saved PDF page as image", extra={"path": path})

        logger.info("PDF conversion complete", extra={"file_path": file_path, "pages": len(images)})
        return image_paths

    except Exception as e:
        logger.exception("PDF to image conversion failed", extra={"file_path": file_path})
        raise


def docx_to_images(file_path: str):
    """
    Convert a DOCX file to a single PNG image of text.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        List containing the generated PNG image path.
    """
    try:
        logger.info("Converting DOCX to image", extra={"file_path": file_path})
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

        if not text:
            logger.warning("DOCX file contains no text", extra={"file_path": file_path})
            text = "[No text found]"

        # Create image
        img = Image.new("RGB", (1200, 1600), "white")
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), text[:5000], fill="black")  # truncate very long text

        path = os.path.join(TEMP_IMG_DIR, f"{os.path.basename(file_path)}.png")
        img.save(path)
        logger.info("DOCX converted to image", extra={"path": path})

        return [path]

    except Exception as e:
        logger.exception("DOCX to image conversion failed", extra={"file_path": file_path})
        raise