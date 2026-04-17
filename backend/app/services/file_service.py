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

def clean_upload_dir(exclude: set[str] = None):
    """
    Cleans all files/folders in UPLOAD_DIR except excluded ones.
    In 'rubric-images', only non-image files are removed.
    """
    exclude = exclude or set()
    image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

    try:
        if not os.path.exists(UPLOAD_DIR):
            return

        for item in os.listdir(UPLOAD_DIR):
            if item in exclude:
                continue

            item_path = os.path.join(UPLOAD_DIR, item)

            try:
                if item == "rubric-images" and os.path.isdir(item_path):
                    for sub_item in os.listdir(item_path):
                        sub_path = os.path.join(item_path, sub_item)

                        try:
                            if os.path.isdir(sub_path):
                                shutil.rmtree(sub_path)
                                continue

                            ext = os.path.splitext(sub_item.strip())[1].lower()

                            logger.debug(f"Processing: {sub_item}, ext: {ext}")

                            if ext in image_exts:
                                logger.debug(f"Keeping image: {sub_path}")
                                continue

                            os.remove(sub_path)
                            logger.info(f"Deleted: {sub_path}")

                        except Exception as e:
                            logger.exception(f"Failed to delete: {sub_path} | Error: {e}")

                else:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)

            except Exception:
                logger.exception(f"Failed to delete: {item_path}")

    except Exception:
        logger.exception("Failed to clean upload directory")

def save_file(file: UploadFile, folder: str):
    try:
        dir_path = os.path.join(UPLOAD_DIR, folder)
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

def process_file(file_path: str, folder: str | None = None):
    try:
        ext = get_file_extension(file_path)

        if folder is not None:
            folder = os.path.join(UPLOAD_DIR, folder)
            os.makedirs(folder, exist_ok=True)

        if ext in ["png", "jpg", "jpeg"]:
            return [file_path]

        elif ext == "pdf":
            if folder is not None:
                return pdf_to_images(file_path, folder=folder)
            return pdf_to_images(file_path)

        elif ext == "docx":
            if folder is not None:
                return docx_to_images(file_path, folder=folder)
            return docx_to_images(file_path)

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


def pdf_to_images(file_path: str, folder: str | None = None):
    """
    Convert a PDF file to a list of PNG images.

    Args:
        file_path: Path to the PDF file.
        folder: Optional folder to also save images.

    Returns:
        List of generated PNG image paths (TEMP dir paths).
    """
    try:
        logger.info("Converting PDF to images", extra={"file_path": file_path})
        images = convert_from_path(file_path)
        image_paths = []

        for i, img in enumerate(images):
            os.makedirs(TEMP_IMG_DIR, exist_ok=True)

            if folder is not None:
                os.makedirs(folder, exist_ok=True)

            filename = f"{uuid.uuid4().hex}.png"
            path = os.path.join(TEMP_IMG_DIR, filename)

            img.save(path, "PNG")
            logger.debug("Saved PDF page as image", extra={"path": path})

            if folder is not None:
                folder_path = os.path.join(folder, filename)
                img.save(folder_path, "PNG")
                logger.debug("Saved copy to folder", extra={"path": folder_path})
                image_paths.append(folder_path)
            else:
                image_paths.append(path)

        logger.info("PDF conversion complete", extra={"file_path": file_path, "pages": len(images)})
        return image_paths

    except Exception as e:
        logger.exception("PDF to image conversion failed", extra={"file_path": file_path})
        raise


def docx_to_images(file_path: str, folder: str | None = None):
    """
    Convert a DOCX file to multiple PNG images (chunked text).

    Args:
        file_path: Path to the DOCX file.
        folder: Optional folder to also save images.

    Returns:
        List of generated PNG image paths.
    """
    try:
        logger.info("Converting DOCX to images", extra={"file_path": file_path})

        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

        if not paragraphs:
            logger.warning("DOCX file contains no text", extra={"file_path": file_path})
            paragraphs = ["[No text found]"]

        full_text = "\n".join(paragraphs)
        chunk_size = 2000  
        text_chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)]

        image_paths = []

        os.makedirs(TEMP_IMG_DIR, exist_ok=True)
        if folder is not None:
            os.makedirs(folder, exist_ok=True)

        for i, chunk in enumerate(text_chunks):
            img = Image.new("RGB", (1200, 1600), "white")
            draw = ImageDraw.Draw(img)

            draw.text((50, 50), chunk, fill="black")

            filename = f"{uuid.uuid4().hex}.png"
            temp_path = os.path.join(TEMP_IMG_DIR, filename)

            img.save(temp_path, "PNG")
            logger.debug("Saved DOCX chunk as image", extra={"path": temp_path})

            if folder is not None:
                folder_path = os.path.join(folder, filename)
                img.save(folder_path, "PNG")
                logger.debug("Saved copy to folder", extra={"path": folder_path})
                image_paths.append(folder_path)
            else:
                image_paths.append(temp_path)

        logger.info(
            "DOCX conversion complete",
            extra={"file_path": file_path, "pages": len(text_chunks)}
        )

        return image_paths

    except Exception:
        logger.exception("DOCX to image conversion failed", extra={"file_path": file_path})
        raise