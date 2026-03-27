# Yu-Gi-Oh! Card Manager (Desktop, Python, Windows)

Produktionsreife Desktop-Anwendung zur Verwaltung von Yu-Gi-Oh!-Karten mit:
- Webcam-Scanner (Einzel + Live/Bulk)
- OCR via Tesseract
- API-Abgleich über YGOPRODeck
- SQLite-Speicherung
- Sammlung, Filter, globale Karten-Datenbank, Deck Builder

## 1) Projektstruktur

```text
card-scanner-yugioh/
├─ app.py
├─ requirements.txt
├─ .gitignore
├─ README.md
└─ ygo_manager/
   ├─ __init__.py
   ├─ config.py
   ├─ main.py
   ├─ api/
   │  └─ ygopro_client.py
   ├─ database/
   │  └─ db.py
   ├─ models/
   │  ├─ card.py
   │  └─ deck.py
   ├─ scanner/
   │  ├─ ocr.py
   │  ├─ preprocess.py
   │  └─ webcam_scanner.py
   ├─ services/
   │  ├─ card_database_service.py
   │  ├─ card_matcher.py
   │  ├─ collection_service.py
   │  └─ deck_service.py
   ├─ ui/
   │  ├─ main_window.py
   │  ├─ styles.py
   │  └─ tabs/
   │     ├─ scanner_tab.py
   │     ├─ collection_tab.py
   │     ├─ card_database_tab.py
   │     └─ deck_builder_tab.py
   └─ utils/
      └─ logging_config.py
```

## 2) Setup & Installation (Windows)

### 2.1 Python installieren
1. Python 3.11+ installieren: https://www.python.org/downloads/windows/
2. Bei der Installation **"Add Python to PATH"** aktivieren.

### 2.2 Projekt vorbereiten
```powershell
git clone <DEIN_REPO_URL>
cd card-scanner-yugioh
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2.3 Tesseract OCR installieren
1. Tesseract für Windows installieren (z. B. UB Mannheim Build).
2. Standardpfad prüfen: `C:\Program Files\Tesseract-OCR\tesseract.exe`
3. Falls nötig in `ygo_manager/config.py` `TESSERACT_CMD` anpassen.

## 3) Anwendung starten

```powershell
python app.py
```

## 4) Nutzung

### Scanner
1. Tab **Scanner** öffnen.
2. **Webcam starten**.
3. **Einzel-Scan** für einzelne Karte oder **Live-Scan Start/Stop** für kontinuierliches Scannen.
4. OCR-Text wird mit Fuzzy Matching normalisiert und via API validiert.
5. Treffer werden automatisch in SQLite gespeichert.

### Sammlung
- Tab **Sammlung** zeigt alle gescannten Karten.
- Anzahl ändern, löschen, Duplikate zusammenführen.

### Karten-Datenbank
- Tab **Karten-Datenbank** lädt alle Karten über die API.
- Filter nach Kartentyp, Attribut, Set, Seltenheit, Freitextsuche (live).

### Deck Builder
- Karten aus Sammlung + globaler Datenbank hinzufügen/entfernen.
- Deck speichern/laden.
- Statistiken: Kartenanzahl + Typverteilung.

## 5) Build zu .exe (PyInstaller)

```powershell
pip install pyinstaller
pyinstaller --noconfirm --name "YGOCardManager" --windowed app.py
```

Die ausführbare Datei liegt anschließend unter:

```text
dist/YGOCardManager/YGOCardManager.exe
```

## 6) Produktions-Hinweise / Best Practices

- Logging: `logs/app.log`
- API-Fallback: Wenn verfügbar wird ein lokaler Cache unter `data/all_cards_cache.json` verwendet.
- Performance: Live-Scan arbeitet intervallbasiert (`QTimer`), statt UI zu blockieren.
- Erweiterbarkeit:
  - Neue Erkennungsmodelle in `scanner/`
  - Cloud-Sync in `services/`
  - Zusätzliche UI-Module in `ui/tabs/`

## 7) Troubleshooting

- **Webcam wird nicht geöffnet:** Kameraindex prüfen (0/1), andere Apps schließen.
- **OCR erkennt schlecht:** bessere Beleuchtung, Karte ruhiger halten, `preprocess.py` feinjustieren.
- **Keine API-Daten:** Internet prüfen; App nutzt ggf. lokalen Cache.
- **Tesseract-Fehler:** Pfad in `config.py` kontrollieren.
