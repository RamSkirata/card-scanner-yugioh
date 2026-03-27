class CardDatabaseService:
    def __init__(self, api_client):
        self.api_client = api_client
        self.cards = []

    def load(self, refresh: bool = False) -> list[dict]:
        self.cards = self.api_client.fetch_all_cards(refresh=refresh)
        return self.cards

    def filter_cards(
        self,
        text: str = "",
        card_type: str = "",
        attribute: str = "",
        set_name: str = "",
        rarity: str = "",
    ) -> list[dict]:
        text = text.lower().strip()
        out = []
        for card in self.cards:
            c_type = (card.get("type") or "").lower()
            c_attr = (card.get("attribute") or "").lower()
            card_sets = card.get("card_sets") or []
            c_set = (card_sets[0].get("set_name") if card_sets else "") or ""
            c_rarity = (card_sets[0].get("set_rarity") if card_sets else "") or ""
            name = (card.get("name") or "").lower()

            if text and text not in name:
                continue
            if card_type and card_type.lower() not in c_type:
                continue
            if attribute and attribute.lower() != c_attr:
                continue
            if set_name and set_name.lower() not in c_set.lower():
                continue
            if rarity and rarity.lower() not in c_rarity.lower():
                continue
            out.append(card)
        return out
