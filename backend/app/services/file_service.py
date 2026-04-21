import os
from pdf2image import convert_from_path
from docx import Document
from PIL import Image, ImageDraw
from app.config.log_config import logger
import uuid
from fastapi import UploadFile
import shutil

UPLOAD_DIR = "uploads"
TEMP_IMG_DIR = os.path.join(UPLOAD_DIR, "temp_images")
TEMP_DIR = os.path.join(UPLOAD_DIR, "temp")
REQUIRED_DIR = os.path.join(UPLOAD_DIR, "required")

def clean_upload_dir():
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
            os.makedirs(TEMP_DIR, exist_ok=True)

        logger.info("Temp upload directory cleaned")

    except Exception:
        logger.exception("Failed to clean temp directory")

def save_file(file: UploadFile, folder: str , storage_type: str = "temp"):
    try:
        base_dir = TEMP_DIR if storage_type == "temp" else REQUIRED_DIR

        dir_path = os.path.join(base_dir, folder)
        os.makedirs(dir_path, exist_ok=True)

        name, ext = os.path.splitext(file.filename)
        new_filename = f"{uuid.uuid4().hex}{ext}"

        path = os.path.join(dir_path, new_filename)

        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        return path

    except Exception:
        logger.exception("File saving failed", extra={"uploaded_filename": file.filename})
        raise

def process_file(file_path: str, folder: str , storage_type: str = "temp"):
    try:
        base_dir = TEMP_DIR if storage_type == "temp" else REQUIRED_DIR
        ext = get_file_extension(file_path)

        dir_path = os.path.join(base_dir, folder)
        os.makedirs(dir_path, exist_ok=True)

        if ext in ["png", "jpg", "jpeg"]:
            filename = os.path.basename(file_path)
            new_filename = f"{uuid.uuid4().hex}.{ext}"
            new_path = os.path.join(dir_path, new_filename)
            shutil.copy(file_path, new_path)
            return [new_path]

        elif ext == "pdf":
            return pdf_to_images(file_path, folder, storage_type)

        elif ext == "docx":
            return docx_to_images(file_path, folder, storage_type)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception:
        logger.exception("File processing failed", extra={"file_path": file_path})
        raise

def get_file_extension(filename: str):
    """Return the lowercase file extension."""
    try:
        ext = filename.lower().split(".")[-1]
        logger.debug(f"Detected file extension: {ext}", extra={"filename": filename})
        return ext
    except Exception as e:
        logger.exception("Failed to get file extension", extra={"filename": filename})
        raise


def pdf_to_images(file_path: str, folder: str, storage_type: str = "temp"):
    """
    Convert a PDF file to a list of PNG images.

    Args:
        file_path: Path to the PDF file.
        folder: folder to also save images.

    Returns:
        List of generated PNG image paths (TEMP dir paths).
    """
    try:
        base_dir = TEMP_DIR if storage_type == "temp" else REQUIRED_DIR
        logger.info("Converting PDF to images", extra={"file_path": file_path})

        dir_path = os.path.join(base_dir, folder)
        
        images = convert_from_path(file_path)
        image_paths = []

        for i, img in enumerate(images):

            filename = f"{uuid.uuid4().hex}.png"
            path = os.path.join(dir_path, filename)

            img.save(path, "PNG")
            logger.debug("Saved PDF page as image", extra={"path": path})

            image_paths.append(path)

        logger.info("PDF conversion complete", extra={"file_path": file_path, "pages": len(images)})
        return image_paths

    except Exception as e:
        logger.exception("PDF to image conversion failed", extra={"file_path": file_path})
        raise


def docx_to_images(file_path: str, folder: str, storage_type: str = "temp"):
    """
    Convert a DOCX file to multiple PNG images (chunked text).

    Args:
        file_path: Path to the DOCX file.
        folder: Optional folder to also save images.

    Returns:
        List of generated PNG image paths.
    """
    try:
        base_dir = TEMP_DIR if storage_type == "temp" else REQUIRED_DIR
        logger.info("Converting DOCX to images", extra={"file_path": file_path})
        dir_path = os.path.join(base_dir, folder)

        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

        if not paragraphs:
            logger.warning("DOCX file contains no text", extra={"file_path": file_path})
            paragraphs = ["[No text found]"]

        full_text = "\n".join(paragraphs)
        chunk_size = 2000  
        text_chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)]

        image_paths = []

        for i, chunk in enumerate(text_chunks):
            img = Image.new("RGB", (1200, 1600), "white")
            draw = ImageDraw.Draw(img)

            draw.text((50, 50), chunk, fill="black")

            filename = f"{uuid.uuid4().hex}.png"
            temp_path = os.path.join(dir_path, filename)

            img.save(temp_path, "PNG")
            logger.debug("Saved DOCX chunk as image", extra={"path": temp_path})

            image_paths.append(temp_path)

        logger.info(
            "DOCX conversion complete",
            extra={"file_path": file_path, "pages": len(text_chunks)}
        )

        return image_paths

    except Exception:
        logger.exception("DOCX to image conversion failed", extra={"file_path": file_path})
        raise