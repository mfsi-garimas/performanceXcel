# app/services/ocr_service.py
import os
import json
from paddleocr import PaddleOCR
from app.config.log_config import logger

# Initialize PaddleOCR once
ocr = PaddleOCR(
    lang='en',
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

def run_ocr(input_path: str, output_folder: str = None) -> str:
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
            raise ValueError(f"Invalid input path: {input_path}")

        if output_folder:
            os.makedirs(output_folder, exist_ok=True)
            logger.debug(f"Output folder created: {output_folder}")

        for file_path in files:
            filename = os.path.basename(file_path)
            logger.info("Processing OCR file", extra={"file": filename})

            try:
                result = ocr.predict(file_path)
            except Exception as e:
                logger.exception("OCR prediction failed", extra={"file": filename})
                continue

            for res in result:
                if isinstance(res, dict) and "rec_texts" in res:
                    all_text_lines.extend(res["rec_texts"])

            if output_folder:
                for i, res in enumerate(result):
                    try:
                        if hasattr(res, "save_to_img"):
                            save_path = os.path.join(output_folder, f"{filename}_annotated_{i}.jpg")
                            res.save_to_img(save_path)
                            logger.debug("Saved annotated image", extra={"path": save_path})
                        if hasattr(res, "save_to_json"):
                            res.save_to_json(output_folder)
                            logger.debug("Saved OCR JSON for image", extra={"folder": output_folder})
                    except Exception as e:
                        logger.warning("Skipping save for file", extra={"file": filename, "error": str(e)})

        combined_text = " ".join(line.strip() for line in all_text_lines)
        logger.info("OCR extraction complete", extra={"file_count": len(files), "lines_extracted": len(all_text_lines)})

        if output_folder:
            try:
                text_json_path = os.path.join(output_folder, "text_only.json")
                with open(text_json_path, "w", encoding="utf-8") as f:
                    json.dump(all_text_lines, f, indent=2, ensure_ascii=False)
                logger.debug("Saved text_only.json", extra={"path": text_json_path})

                text_combined_path = os.path.join(output_folder, "text_combined.txt")
                with open(text_combined_path, "w", encoding="utf-8") as f:
                    f.write(combined_text)
                logger.debug("Saved text_combined.txt", extra={"path": text_combined_path})
            except Exception as e:
                logger.exception("Failed to save OCR output files", extra={"output_folder": output_folder})

        return combined_text

    except Exception as e:
        logger.exception("OCR process failed", extra={"input_path": input_path})
        raise