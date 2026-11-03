"""Small SQLite conversation store; credentials are deliberately not stored here."""
import sqlite3
from pathlib import Path
from typing import Any

class Store:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, conversation_id TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('user','assistant')), content TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))) ")

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        return db

    def append(self, conversation_id: str, role: str, content: str) -> None:
        if role not in {"user", "assistant"}:
            raise ValueError("unsupported role")
        with self._connect() as db:
            db.execute("INSERT INTO messages(conversation_id,role,content) VALUES(?,?,?)", (conversation_id, role, content))

    def recent(self, conversation_id: str, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT role,content,created_at FROM (SELECT role,content,created_at,id FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT ?) ORDER BY id", (conversation_id, limit)).fetchall()
        return [dict(row) for row in rows]

    def clear(self, conversation_id: str) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM messages WHERE conversation_id=?", (conversation_id,))
