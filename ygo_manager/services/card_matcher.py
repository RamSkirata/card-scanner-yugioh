from rapidfuzz import fuzz, process


class CardMatcher:
    def __init__(self, card_names: list[str]):
        self.card_names = card_names

    def best_match(self, raw_text: str, cutoff: int = 65) -> str | None:
        if not raw_text or not self.card_names:
            return None
        match = process.extractOne(
            raw_text,
            self.card_names,
            scorer=fuzz.WRatio,
            score_cutoff=cutoff,
        )
        return match[0] if match else None
