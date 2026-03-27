from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CardDatabaseTab(QWidget):
    def __init__(self, card_db_service):
        super().__init__()
        self.card_db_service = card_db_service
        self.cards = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        filter_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Freitextsuche...")
        self.type_filter = QLineEdit()
        self.type_filter.setPlaceholderText("Kartentyp")
        self.attr_filter = QComboBox()
        self.attr_filter.addItems(["", "DARK", "LIGHT", "EARTH", "WATER", "FIRE", "WIND", "DIVINE"])
        self.set_filter = QLineEdit()
        self.set_filter.setPlaceholderText("Set")
        self.rarity_filter = QLineEdit()
        self.rarity_filter.setPlaceholderText("Seltenheit")
        self.btn_load = QPushButton("Karten laden")

        self.search.textChanged.connect(self.apply_filters)
        self.type_filter.textChanged.connect(self.apply_filters)
        self.attr_filter.currentTextChanged.connect(self.apply_filters)
        self.set_filter.textChanged.connect(self.apply_filters)
        self.rarity_filter.textChanged.connect(self.apply_filters)
        self.btn_load.clicked.connect(self.load_cards)

        for widget in [
            QLabel("Suche:"),
            self.search,
            QLabel("Typ:"),
            self.type_filter,
            QLabel("Attribut:"),
            self.attr_filter,
            self.set_filter,
            self.rarity_filter,
            self.btn_load,
        ]:
            filter_row.addWidget(widget)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Name", "Typ", "Attribut", "Set", "Seltenheit"])

        layout.addLayout(filter_row)
        layout.addWidget(self.table)

    def load_cards(self):
        self.cards = self.card_db_service.load(refresh=False)
        self.apply_filters()

    def apply_filters(self):
        filtered = self.card_db_service.filter_cards(
            text=self.search.text(),
            card_type=self.type_filter.text(),
            attribute=self.attr_filter.currentText(),
            set_name=self.set_filter.text(),
            rarity=self.rarity_filter.text(),
        )
        self.table.setRowCount(min(len(filtered), 1000))
        for i, card in enumerate(filtered[:1000]):
            sets = card.get("card_sets") or []
            set_name = sets[0].get("set_name") if sets else ""
            rarity = sets[0].get("set_rarity") if sets else ""
            values = [card.get("name", ""), card.get("type", ""), card.get("attribute", ""), set_name, rarity]
            for j, val in enumerate(values):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
