# repos/room_repo.py
from core.db import memory_db
from datetime import datetime

class RoomRepo:
    def create_table(self):
        """Create the rooms table if it doesn’t exist."""
        query = """
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL UNIQUE,
            floor_no INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
        """
        memory_db.execute(query)

    def create(self, room_name: str, floor_no: int):
        """Insert a new room."""
        query = """
        INSERT INTO rooms (room_name, floor_no, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        """
        now = datetime.now().isoformat(timespec="seconds")
        return memory_db.execute(query, (room_name, floor_no, now, now))

    def get_all(self):
        """Fetch all rooms."""
        return memory_db.fetch_all("SELECT * FROM rooms")

    def get_by_name(self, room_name: str):
        """Fetch a specific room by name."""
        return memory_db.fetch_one("SELECT * FROM rooms WHERE room_name = ?", (room_name,))
