from dataclasses import dataclass, field


@dataclass
class Deck:
    name: str
    cards: dict[str, int] = field(default_factory=dict)

    def add_card(self, card_name: str, amount: int = 1) -> None:
        self.cards[card_name] = self.cards.get(card_name, 0) + amount

    def remove_card(self, card_name: str, amount: int = 1) -> None:
        if card_name not in self.cards:
            return
        self.cards[card_name] -= amount
        if self.cards[card_name] <= 0:
            del self.cards[card_name]
