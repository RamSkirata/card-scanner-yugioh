import json

from ygo_manager.models.deck import Deck


class DeckService:
    def __init__(self, db):
        self.db = db

    def save_deck(self, deck: Deck) -> None:
        self.db.save_deck(deck.name, json.dumps(deck.cards))

    def list_decks(self) -> list[dict]:
        rows = self.db.list_decks()
        for row in rows:
            row["cards"] = json.loads(row["payload"])
        return rows
