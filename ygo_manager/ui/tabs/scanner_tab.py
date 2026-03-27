import logging

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ygo_manager.models.card import Card

logger = logging.getLogger(__name__)


class ScannerTab(QWidget):
    def __init__(self, scanner, api_client, matcher, collection_service):
        super().__init__()
        self.scanner = scanner
        self.api_client = api_client
        self.matcher = matcher
        self.collection_service = collection_service
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._scan_tick)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        self.status_label = QLabel("Scanner bereit.")
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        row = QHBoxLayout()
        self.btn_start = QPushButton("Webcam starten")
        self.btn_single = QPushButton("Einzel-Scan")
        self.btn_live = QPushButton("Live-Scan Start/Stop")
        self.btn_start.clicked.connect(self.toggle_camera)
        self.btn_single.clicked.connect(self.scan_once)
        self.btn_live.clicked.connect(self.toggle_live_scan)

        for b in (self.btn_start, self.btn_single, self.btn_live):
            row.addWidget(b)

        layout.addLayout(row)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_box)

    def toggle_camera(self):
        if self.scanner.capture:
            self.scanner.close()
            self.status_label.setText("Webcam gestoppt.")
            return
        ok = self.scanner.open(0)
        self.status_label.setText("Webcam aktiv." if ok else "Webcam konnte nicht geöffnet werden.")

    def toggle_live_scan(self):
        if self.timer.isActive():
            self.timer.stop()
            self.status_label.setText("Live-Scan gestoppt.")
            return
        if not self.scanner.capture and not self.scanner.open(0):
            QMessageBox.warning(self, "Fehler", "Webcam nicht verfügbar.")
            return
        self.timer.start(1200)
        self.status_label.setText("Live-Scan läuft...")

    def scan_once(self):
        text, _ = self.scanner.scan_once()
        self._handle_text(text)

    def _scan_tick(self):
        text, _ = self.scanner.scan_once()
        self._handle_text(text)

    def _handle_text(self, text: str | None):
        if not text:
            return
        match = self.matcher.best_match(text)
        target = match or text
        card_payload = self.api_client.search_by_name(target)
        if not card_payload:
            self.result_box.append(f"Nicht gefunden: OCR='{text}'")
            return
        card = Card.from_api(card_payload)
        self.collection_service.add_card(card)
        self.result_box.append(f"Gespeichert: {card.name} ({card.set_name})")
