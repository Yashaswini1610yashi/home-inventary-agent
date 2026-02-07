# repos/user_repo.py
from core.db import memory_db
from datetime import datetime

class UserRepo:
    def __init__(self):
        self.ensure_table()

    def ensure_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            full_name TEXT,
            email TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """
        memory_db.execute(query)

    def get_all(self):
        return memory_db.fetch_all("SELECT * FROM users")

    def get_by_username(self, username: str):
        return memory_db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))

    def create(self, user_data: dict):
        now = datetime.now().isoformat(timespec="seconds")
        return memory_db.execute(
            "INSERT INTO users (username, full_name, email, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (user_data["username"], user_data.get("full_name"), user_data.get("email"), now, now)
        )

    def update(self, username: str, user_data: dict):
        now = datetime.now().isoformat(timespec="seconds")
        return memory_db.execute(
            "UPDATE users SET full_name = ?, email = ?, updated_at = ? WHERE username = ?",
            (user_data.get("full_name"), user_data.get("email"), now, username)
        )

    def delete(self, username: str):
        return memory_db.execute("DELETE FROM users WHERE username = ?", (username,))
