from PyQt6.QtWidgets import QMainWindow, QTabWidget

from ygo_manager.ui.styles import DARK_STYLESHEET
from ygo_manager.ui.tabs.card_database_tab import CardDatabaseTab
from ygo_manager.ui.tabs.collection_tab import CollectionTab
from ygo_manager.ui.tabs.deck_builder_tab import DeckBuilderTab
from ygo_manager.ui.tabs.scanner_tab import ScannerTab


class MainWindow(QMainWindow):
    def __init__(self, scanner, api_client, matcher, collection_service, card_db_service, deck_service):
        super().__init__()
        self.setWindowTitle("Yu-Gi-Oh! Card Manager")
        self.resize(1300, 800)
        self.setStyleSheet(DARK_STYLESHEET)

        tabs = QTabWidget()
        self.scanner_tab = ScannerTab(scanner, api_client, matcher, collection_service)
        self.collection_tab = CollectionTab(collection_service)
        self.card_db_tab = CardDatabaseTab(card_db_service)
        self.deck_tab = DeckBuilderTab(collection_service, card_db_service, deck_service)

        tabs.addTab(self.scanner_tab, "Scanner")
        tabs.addTab(self.collection_tab, "Sammlung")
        tabs.addTab(self.card_db_tab, "Karten-Datenbank")
        tabs.addTab(self.deck_tab, "Deck Builder")

        self.setCentralWidget(tabs)
