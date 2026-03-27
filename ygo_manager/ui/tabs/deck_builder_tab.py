from collections import Counter

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ygo_manager.models.deck import Deck


class DeckBuilderTab(QWidget):
    def __init__(self, collection_service, card_db_service, deck_service):
        super().__init__()
        self.collection_service = collection_service
        self.card_db_service = card_db_service
        self.deck_service = deck_service
        self.current_deck = Deck(name="Neues Deck")
        self._build_ui()
        self.refresh_sources()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.deck_name = QLineEdit("Neues Deck")
        self.btn_save = QPushButton("Deck speichern")
        self.btn_load = QPushButton("Gespeicherte Decks laden")
        self.btn_save.clicked.connect(self.save_deck)
        self.btn_load.clicked.connect(self.load_decks)
        top.addWidget(QLabel("Deckname:"))
        top.addWidget(self.deck_name)
        top.addWidget(self.btn_save)
        top.addWidget(self.btn_load)

        mid = QHBoxLayout()
        self.source_cards = QListWidget()
        self.deck_cards = QListWidget()
        self.btn_add = QPushButton(">>")
        self.btn_remove = QPushButton("<<")
        self.btn_add.clicked.connect(self.add_card)
        self.btn_remove.clicked.connect(self.remove_card)

        controls = QVBoxLayout()
        controls.addWidget(self.btn_add)
        controls.addWidget(self.btn_remove)

        mid.addWidget(self.source_cards)
        mid.addLayout(controls)
        mid.addWidget(self.deck_cards)

        self.stats = QTextEdit()
        self.stats.setReadOnly(True)

        layout.addLayout(top)
        layout.addLayout(mid)
        layout.addWidget(self.stats)

    def refresh_sources(self):
        self.source_cards.clear()
        owned = [f"{c['name']} (Collection x{c['count']})" for c in self.collection_service.list_cards()]
        global_cards = [c.get("name", "") for c in self.card_db_service.cards[:200]]
        self.source_cards.addItems(owned + global_cards)

    def add_card(self):
        item = self.source_cards.currentItem()
        if not item:
            return
        card_name = item.text().split(" (Collection")[0]
        self.current_deck.add_card(card_name)
        self.render_deck()

    def remove_card(self):
        item = self.deck_cards.currentItem()
        if not item:
            return
        card_name = item.text().rsplit(" x", 1)[0]
        self.current_deck.remove_card(card_name)
        self.render_deck()

    def render_deck(self):
        self.deck_cards.clear()
        for name, count in sorted(self.current_deck.cards.items()):
            self.deck_cards.addItem(f"{name} x{count}")
        self._update_stats()

    def _update_stats(self):
        total = sum(self.current_deck.cards.values())
        type_counter = Counter()
        for name in self.current_deck.cards:
            for card in self.card_db_service.cards:
                if card.get("name") == name:
                    type_counter[card.get("type", "Unknown")] += self.current_deck.cards[name]
                    break
        self.stats.setText(
            f"Anzahl Karten: {total}\nTypverteilung:\n" + "\n".join(f"- {k}: {v}" for k, v in type_counter.items())
        )

    def save_deck(self):
        self.current_deck.name = self.deck_name.text().strip() or "Neues Deck"
        self.deck_service.save_deck(self.current_deck)

    def load_decks(self):
        decks = self.deck_service.list_decks()
        self.stats.append("\nGespeicherte Decks:")
        for d in decks:
            self.stats.append(f"- {d['name']} ({sum(d['cards'].values())} Karten)")
