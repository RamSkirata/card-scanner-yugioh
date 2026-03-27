import logging

import pytesseract

from ygo_manager.config import TESSERACT_CMD

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

    def extract_text(self, image) -> str:
        try:
            text = pytesseract.image_to_string(image, config="--psm 7")
            return text.strip()
        except Exception as exc:  # pragma: no cover
            logger.error("OCR failed: %s", exc)
            return ""
