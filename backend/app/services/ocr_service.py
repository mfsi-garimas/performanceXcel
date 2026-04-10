import os
import json
from paddleocr import PPStructureV3
from app.config.log_config import logger

ocr = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

def run_ocr(input_path: str, output_folder: str = None) -> str:
    logger.info("Starting OCR process", extra={"input_path": input_path, "output_folder": output_folder})
    try:
        all_text_lines = []

        if os.path.isfile(input_path):
            files = [input_path]
        elif os.path.isdir(input_path):
            files = [
                os.path.join(input_path, f)
                for f in sorted(os.listdir(input_path))
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]
        else:
            logger.error("Invalid input path provided", extra={"input_path": input_path})
            raise ValueError(f"Invalid input path: {input_path}")

        if output_folder:
            os.makedirs(output_folder, exist_ok=True)
            logger.debug("Output folder ensured", extra={"output_folder": output_folder})

        structured_HTML = []
        structured_TEXT = []

        for file_path in files:
            file_name = os.path.basename(file_path)
            logger.info("Processing OCR file", extra={"file_name": file_name})

            try:
                result = ocr.predict(input=file_path)
                logger.debug("OCR prediction successful", extra={"file_name": file_name})
            except Exception as e:
                logger.exception("OCR prediction failed", extra={"file_name": file_name})
                continue

            for item in result:
                ocr_res = item.get("overall_ocr_res", {})
                rec_texts = ocr_res.get("rec_texts", [])
                if rec_texts:
                    structured_TEXT.extend(rec_texts)
                    logger.debug("Extracted recognized texts", extra={"file_name": file_name, "texts_count": len(rec_texts)})

                for table in item.get("table_res_list", []):
                    table_html = table.get("pred_html") if isinstance(table, dict) else getattr(table, "pred_html", None)
                    if table_html:
                        structured_HTML.append(table_html.strip())
                        logger.debug("Extracted table HTML", extra={"file_name": file_name})

        combined_TEXT = "\n".join(line.strip() for line in structured_TEXT if line.strip())
        combined_HTML = "\n".join(line.strip() for line in structured_HTML if line.strip())

        combined_result = {
            "ocr_text": combined_TEXT,
            "table_html": combined_HTML
        }
        return combined_result

    except Exception as e:
        logger.exception("OCR process failed", extra={"input_path": input_path})
        raise e