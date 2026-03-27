import logging
import time

import cv2

from ygo_manager.scanner.preprocess import preprocess_for_ocr

logger = logging.getLogger(__name__)


class WebcamScanner:
    def __init__(self, ocr_service):
        self.ocr_service = ocr_service
        self.capture = None

    def open(self, camera_index: int = 0) -> bool:
        self.capture = cv2.VideoCapture(camera_index)
        ok = bool(self.capture and self.capture.isOpened())
        if not ok:
            logger.error("Could not open webcam.")
        return ok

    def close(self) -> None:
        if self.capture:
            self.capture.release()
            self.capture = None

    def read_frame(self):
        if not self.capture:
            return None
        ok, frame = self.capture.read()
        return frame if ok else None

    def scan_once(self) -> tuple[str, any] | tuple[None, None]:
        frame = self.read_frame()
        if frame is None:
            return None, None
        processed = preprocess_for_ocr(frame)
        text = self.ocr_service.extract_text(processed)
        return text, frame

    def scan_live(self, callback, interval_s: float = 1.0, max_scans: int = 200) -> None:
        scans = 0
        while scans < max_scans and self.capture and self.capture.isOpened():
            text, frame = self.scan_once()
            if text:
                callback(text, frame)
            scans += 1
            time.sleep(interval_s)
