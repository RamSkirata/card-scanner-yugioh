from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CollectionTab(QWidget):
    def __init__(self, collection_service):
        super().__init__()
        self.collection_service = collection_service
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.btn_refresh = QPushButton("Aktualisieren")
        self.btn_delete = QPushButton("Ausgewählte löschen")
        self.btn_merge = QPushButton("Duplikate zusammenführen")
        self.btn_count = QPushButton("Anzahl setzen")
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 999)

        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_merge.clicked.connect(self.merge_duplicates)
        self.btn_count.clicked.connect(self.update_count)

        for w in (self.btn_refresh, self.btn_delete, self.btn_merge, self.count_spin, self.btn_count):
            top.addWidget(w)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Typ", "Attribut", "Set", "Seltenheit", "Anzahl"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addLayout(top)
        layout.addWidget(self.table)

    def refresh(self):
        cards = self.collection_service.list_cards()
        self.table.setRowCount(len(cards))
        for i, card in enumerate(cards):
            values = [
                card["id"],
                card["name"],
                card["card_type"],
                card["attribute"],
                card["set_name"],
                card["rarity"],
                card["count"],
            ]
            for j, val in enumerate(values):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def _selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return int(item.text()) if item else None

    def delete_selected(self):
        card_id = self._selected_id()
        if card_id is None:
            QMessageBox.information(self, "Info", "Keine Karte ausgewählt")
            return
        self.collection_service.delete(card_id)
        self.refresh()

    def update_count(self):
        card_id = self._selected_id()
        if card_id is None:
            return
        self.collection_service.update_count(card_id, self.count_spin.value())
        self.refresh()

    def merge_duplicates(self):
        self.collection_service.merge_duplicates()
        self.refresh()
