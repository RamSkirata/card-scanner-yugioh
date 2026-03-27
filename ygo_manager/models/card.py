from dataclasses import dataclass
from datetime import datetime


@dataclass
class Card:
    name: str
    card_type: str = "Unknown"
    attribute: str = "Unknown"
    set_name: str = "Unknown"
    rarity: str = "Unknown"
    image_url: str = ""
    count: int = 1
    scanned_at: datetime | None = None

    @classmethod
    def from_api(cls, payload: dict) -> "Card":
        card_sets = payload.get("card_sets") or []
        card_set = card_sets[0] if card_sets else {}
        images = payload.get("card_images") or []
        image = images[0] if images else {}
        return cls(
            name=payload.get("name", "Unknown"),
            card_type=payload.get("type", "Unknown"),
            attribute=payload.get("attribute", "Unknown"),
            set_name=card_set.get("set_name", "Unknown"),
            rarity=card_set.get("set_rarity", "Unknown"),
            image_url=image.get("image_url", ""),
        )
