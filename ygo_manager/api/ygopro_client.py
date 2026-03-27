import json
import logging
from pathlib import Path

import requests

from ygo_manager.config import API_BASE_URL, CARD_CACHE_FILE

logger = logging.getLogger(__name__)


class YGOProClient:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def search_by_name(self, name: str) -> dict | None:
        try:
            response = requests.get(
                f"{API_BASE_URL}/cardinfo.php",
                params={"name": name},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            return data[0] if data else None
        except requests.RequestException as exc:
            logger.error("API search_by_name failed: %s", exc)
            return None

    def fetch_all_cards(self, refresh: bool = False) -> list[dict]:
        if CARD_CACHE_FILE.exists() and not refresh:
            return self._read_cache(CARD_CACHE_FILE)

        try:
            response = requests.get(
                f"{API_BASE_URL}/cardinfo.php", timeout=self.timeout
            )
            response.raise_for_status()
            cards = response.json().get("data", [])
            self._write_cache(CARD_CACHE_FILE, cards)
            return cards
        except requests.RequestException as exc:
            logger.error("API fetch_all_cards failed: %s", exc)
            if CARD_CACHE_FILE.exists():
                return self._read_cache(CARD_CACHE_FILE)
            return []

    @staticmethod
    def _read_cache(path: Path) -> list[dict]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

    @staticmethod
    def _write_cache(path: Path, cards: list[dict]) -> None:
        try:
            path.write_text(json.dumps(cards), encoding="utf-8")
        except OSError as exc:
            logger.warning("Failed to write cache: %s", exc)
