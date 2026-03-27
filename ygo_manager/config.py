from pathlib import Path

APP_NAME = "Yu-Gi-Oh! Card Manager"
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "cards.db"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

TESSERACT_CMD = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
API_BASE_URL = "https://db.ygoprodeck.com/api/v7"
CARD_CACHE_FILE = DATA_DIR / "all_cards_cache.json"
