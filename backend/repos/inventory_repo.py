# repos/inventory_repo.py
from core.db import memory_db
from datetime import datetime

class InventoryRepo:
    def __init__(self):
        # ensure required schema exists and migration runs automatically
        self.ensure_tables()

    def ensure_tables(self):
        # create inventory table if it doesn't exist (room_name included)
        query = """
        CREATE TABLE IF NOT EXISTS inventory (
            item_name TEXT PRIMARY KEY,
            cat_name TEXT,
            item_status TEXT,
            comment TEXT,
            username TEXT,
            last_updated_at TEXT,
            created_at TEXT,
            room_name TEXT
        )
        """
        memory_db.execute(query)
        # rooms table handled by RoomRepo in room_repo.py

    # Core operations
    def get_all(self):
        return memory_db.fetch_all("SELECT * FROM inventory ORDER BY created_at DESC")

    def get_by_name(self, item_name: str):
        return memory_db.fetch_one("SELECT * FROM inventory WHERE item_name = ?", (item_name,))

    def get_by_status(self, status: str):
        return memory_db.fetch_all("SELECT * FROM inventory WHERE LOWER(item_status) = ?", (status.lower(),))

    def get_by_category(self, cat_name: str):
        return memory_db.fetch_all("SELECT * FROM inventory WHERE cat_name = ?", (cat_name,))

    def create(self, item_data: dict):
        query = """
        INSERT INTO inventory (item_name, cat_name, item_status, comment, username, last_updated_at, created_at, room_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            item_data["item_name"],
            item_data.get("cat_name", ""),
            item_data.get("item_status", "").lower(),
            item_data.get("comment", ""),
            item_data.get("username", "admin"),
            item_data.get("last_updated_at") or datetime.now().isoformat(timespec="seconds"),
            item_data.get("created_at") or datetime.now().isoformat(timespec="seconds"),
            item_data.get("room_name")
        )
        return memory_db.execute(query, params)

    def delete(self, item_name: str):
        return memory_db.execute("DELETE FROM inventory WHERE item_name = ?", (item_name,))

    def assign_user(self, item_name: str, username: str):
        query = """
        UPDATE inventory SET username = ?, last_updated_at = ? WHERE item_name = ?
        """
        return memory_db.execute(query, (username, datetime.now().isoformat(timespec="seconds"), item_name))

    def update_status(self, item_name: str, new_status: str):
        query = """
        UPDATE inventory SET item_status = ?, last_updated_at = ? WHERE item_name = ?
        """
        return memory_db.execute(query, (new_status.lower(), datetime.now().isoformat(timespec="seconds"), item_name))

    # Analytics
    def get_total_count(self):
        row = memory_db.fetch_one("SELECT COUNT(*) as total FROM inventory")
        if not row:
            return 0
        return int(row.get("total", 0))

    def get_count_by_category(self, category: str):
        row = memory_db.fetch_one("SELECT COUNT(*) as total FROM inventory WHERE cat_name = ?", (category,))
        if not row:
            return 0
        return int(row.get("total", 0))

    def get_count_by_status(self, status: str):
        row = memory_db.fetch_one("SELECT COUNT(*) as total FROM inventory WHERE LOWER(item_status) = ?", (status.lower(),))
        if not row:
            return 0
        return int(row.get("total", 0))

    def get_user_with_most_items(self):
        row = memory_db.fetch_one(
            "SELECT username, COUNT(*) as cnt FROM inventory GROUP BY username ORDER BY cnt DESC LIMIT 1"
        )
        if not row:
            return None
        return {"username": row.get("username"), "count": int(row.get("cnt", 0))}

    # Auditing
    def get_last_updated_item(self):
        return memory_db.fetch_one(
            "SELECT * FROM inventory WHERE last_updated_at IS NOT NULL AND last_updated_at != '' "
            "ORDER BY last_updated_at DESC LIMIT 1"
        )

    def get_items_not_updated_since(self, cutoff_iso: str):
        return memory_db.fetch_all(
            "SELECT * FROM inventory WHERE last_updated_at IS NULL OR last_updated_at = '' OR last_updated_at < ? "
            "ORDER BY last_updated_at ASC",
            (cutoff_iso,),
        )

    def get_users_with_most_low_status_items(self, limit: int = 10):
        return memory_db.fetch_all(
            "SELECT username, COUNT(*) as cnt FROM inventory WHERE LOWER(item_status) = 'low' "
            "GROUP BY username ORDER BY cnt DESC LIMIT ?",
            (limit,),
        )

    # Room / Multi-modal
    def get_count_by_room_name(self, room_name: str):
        row = memory_db.fetch_one(
            "SELECT COUNT(item_name) as total FROM inventory WHERE room_name = ?",
            (room_name,),
        )
        if not row:
            return 0
        return int(row.get("total", 0))

    def get_room_with_most_high_items(self):
        return memory_db.fetch_one(
            "SELECT room_name, COUNT(item_name) as cnt FROM inventory WHERE LOWER(item_status) = 'high' "
            "GROUP BY room_name ORDER BY cnt DESC LIMIT 1"
        )

    def get_most_recent_updater_for_room(self, room_name: str):
        return memory_db.fetch_one(
            "SELECT username, item_name, last_updated_at FROM inventory "
            "WHERE room_name = ? AND last_updated_at IS NOT NULL ORDER BY last_updated_at DESC LIMIT 1",
            (room_name,),
        )
