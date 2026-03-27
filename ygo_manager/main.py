import logging
import sys

from PyQt6.QtWidgets import QApplication

from ygo_manager.api.ygopro_client import YGOProClient
from ygo_manager.config import DB_PATH
from ygo_manager.database.db import Database
from ygo_manager.scanner.ocr import OCRService
from ygo_manager.scanner.webcam_scanner import WebcamScanner
from ygo_manager.services.card_database_service import CardDatabaseService
from ygo_manager.services.card_matcher import CardMatcher
from ygo_manager.services.collection_service import CollectionService
from ygo_manager.services.deck_service import DeckService
from ygo_manager.ui.main_window import MainWindow
from ygo_manager.utils.logging_config import setup_logging


def build_app() -> QApplication:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Yu-Gi-Oh! Card Manager")

    db = Database(DB_PATH)
    api_client = YGOProClient()
    card_db_service = CardDatabaseService(api_client)
    all_cards = card_db_service.load(refresh=False)
    card_names = [c.get("name", "") for c in all_cards]

    matcher = CardMatcher(card_names)
    collection_service = CollectionService(db)
    deck_service = DeckService(db)

    ocr = OCRService()
    scanner = WebcamScanner(ocr)

    app = QApplication(sys.argv)
    window = MainWindow(
        scanner=scanner,
        api_client=api_client,
        matcher=matcher,
        collection_service=collection_service,
        card_db_service=card_db_service,
        deck_service=deck_service,
    )
    window.show()
    return app


def main() -> int:
    app = build_app()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
