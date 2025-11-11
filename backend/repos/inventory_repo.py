from core.db import memory_db
from datetime import datetime


class InventoryRepo:
    def get_all(self):
        return memory_db.fetch_all("SELECT * FROM inventory ORDER BY created_at DESC")

    def get_by_name(self, item_name: str):
        return memory_db.fetch_one("SELECT * FROM inventory WHERE item_name = ?", (item_name,))

    def get_by_status(self, status: str):
        # ✅ Fix: column name is item_status (not qty_level)
        return memory_db.fetch_all("SELECT * FROM inventory WHERE item_status = ?", (status,))

    def get_by_category(self, cat_name: str):
        return memory_db.fetch_all("SELECT * FROM inventory WHERE cat_name = ?", (cat_name,))

    def create(self, item_data: dict):
        query = """
        INSERT INTO inventory (item_name, cat_name, item_status, comment, username, last_updated_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            item_data["item_name"],
            item_data.get("cat_name", ""),       # allow empty category
            item_data.get("item_status", ""),    # allow empty status
            item_data.get("comment", ""),
            item_data.get("username", "admin"),  # default username if not given
            datetime.now().isoformat(timespec='seconds'),
            datetime.now().isoformat(timespec='seconds')
        )
        return memory_db.execute(query, params)

    def delete(self, item_name: str):
        return memory_db.execute("DELETE FROM inventory WHERE item_name = ?", (item_name,))

