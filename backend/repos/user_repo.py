from core.db import memory_db
from datetime import datetime

class UserRepo:
    def get_all(self):
        return memory_db.fetch_all("SELECT * FROM users")

    def get_by_username(self, username: str):
        return memory_db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))

    def create(self, user_data: dict):
        query = """
        INSERT INTO users (username, firstname, lastname, login_status, password, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            user_data["username"],
            user_data["firstname"],
            user_data["lastname"],
            user_data["login_status"],
            user_data.get("password", ""),
            datetime.now().isoformat(timespec='seconds')
        )
        return memory_db.execute(query, params)

    def update(self, username: str, user_data: dict):
        query = """
        UPDATE users SET firstname=?, lastname=?, login_status=?
        WHERE username=?
        """
        params = (user_data["firstname"], user_data["lastname"], user_data["login_status"], username)
        return memory_db.execute(query, params)

    def delete(self, username: str):
        return memory_db.execute("DELETE FROM users WHERE username=?", (username,))
