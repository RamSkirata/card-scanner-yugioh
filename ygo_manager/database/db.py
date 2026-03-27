import sqlite3
from datetime import datetime
from pathlib import Path


class Database:
    def __init__(self, path: Path):
        self.path = path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS collection (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    card_type TEXT,
                    attribute TEXT,
                    set_name TEXT,
                    rarity TEXT,
                    image_url TEXT,
                    count INTEGER DEFAULT 1,
                    scanned_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS decks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    payload TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def upsert_collection_card(self, card: dict) -> None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, count FROM collection WHERE name = ? AND set_name = ?",
                (card["name"], card.get("set_name", "Unknown")),
            ).fetchone()
            if row:
                conn.execute(
                    "UPDATE collection SET count = ?, scanned_at = ? WHERE id = ?",
                    (row[1] + card.get("count", 1), datetime.utcnow().isoformat(), row[0]),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO collection(name, card_type, attribute, set_name, rarity, image_url, count, scanned_at)
                    VALUES(?,?,?,?,?,?,?,?)
                    """,
                    (
                        card["name"],
                        card.get("card_type", "Unknown"),
                        card.get("attribute", "Unknown"),
                        card.get("set_name", "Unknown"),
                        card.get("rarity", "Unknown"),
                        card.get("image_url", ""),
                        card.get("count", 1),
                        datetime.utcnow().isoformat(),
                    ),
                )

    def list_collection(self) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, name, card_type, attribute, set_name, rarity, image_url, count, scanned_at
                FROM collection ORDER BY scanned_at DESC
                """
            ).fetchall()
        return [
            {
                "id": r[0],
                "name": r[1],
                "card_type": r[2],
                "attribute": r[3],
                "set_name": r[4],
                "rarity": r[5],
                "image_url": r[6],
                "count": r[7],
                "scanned_at": r[8],
            }
            for r in rows
        ]

    def update_count(self, card_id: int, count: int) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE collection SET count = ? WHERE id = ?", (count, card_id))

    def delete_card(self, card_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM collection WHERE id = ?", (card_id,))

    def merge_duplicates(self) -> None:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT name, set_name, SUM(count) FROM collection GROUP BY name, set_name"
            ).fetchall()
            conn.execute("DELETE FROM collection")
            for name, set_name, count in rows:
                conn.execute(
                    """
                    INSERT INTO collection(name, set_name, count, scanned_at)
                    VALUES(?,?,?,?)
                    """,
                    (name, set_name, count, datetime.utcnow().isoformat()),
                )

    def save_deck(self, name: str, payload: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO decks(name, payload, updated_at) VALUES(?,?,?)
                ON CONFLICT(name) DO UPDATE SET payload=excluded.payload, updated_at=excluded.updated_at
                """,
                (name, payload, datetime.utcnow().isoformat()),
            )

    def list_decks(self) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, payload, updated_at FROM decks ORDER BY updated_at DESC"
            ).fetchall()
        return [{"id": r[0], "name": r[1], "payload": r[2], "updated_at": r[3]} for r in rows]
