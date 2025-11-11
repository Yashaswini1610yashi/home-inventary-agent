from core.db import memory_db
from datetime import datetime

class CategoryRepo:
    def get_all(self):
        return memory_db.fetch_all("SELECT * FROM categories")

    def get_by_name(self, cat_name: str):
        return memory_db.fetch_one("SELECT * FROM categories WHERE cat_name=?", (cat_name,))

    def create(self, cat_data: dict):
        memory_db.execute(
            "INSERT INTO categories (cat_name) VALUES (?)",
            (cat_data["cat_name"],)
        )
        
    def delete(self, cat_name: str):
        return memory_db.execute("DELETE FROM categories WHERE cat_name=?", (cat_name,))
