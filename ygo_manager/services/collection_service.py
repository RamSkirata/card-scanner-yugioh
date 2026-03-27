from ygo_manager.models.card import Card


class CollectionService:
    def __init__(self, db):
        self.db = db

    def add_card(self, card: Card) -> None:
        self.db.upsert_collection_card(card.__dict__)

    def list_cards(self) -> list[dict]:
        return self.db.list_collection()

    def update_count(self, card_id: int, count: int) -> None:
        self.db.update_count(card_id, count)

    def delete(self, card_id: int) -> None:
        self.db.delete_card(card_id)

    def merge_duplicates(self) -> None:
        self.db.merge_duplicates()
