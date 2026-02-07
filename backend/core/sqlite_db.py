# core/sqlite_db.py
import sqlite3

class SQLiteDB:
    """Simple synchronous SQLite setup class."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_tables()

    def connect(self):
        """Create connection to DB"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_tables(self):
        """Create the base tables (inventory, users, categories, rooms)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # --- inventory table (minimal set; room_name included for multimodal) ---
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    item_name TEXT PRIMARY KEY,
                    cat_name TEXT,
                    item_status TEXT,
                    comment TEXT,
                    username TEXT,
                    last_updated_at TEXT,
                    created_at TEXT DEFAULT (datetime('now')),
                    room_name TEXT
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    firstname TEXT NOT NULL,
                    lastname TEXT,
                    login_status TEXT CHECK (login_status IN ('enabled', 'disabled')),
                    password TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    cat_name TEXT UNIQUE NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rooms (
                    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name TEXT NOT NULL UNIQUE,
                    floor_no INTEGER,
                    created_at TEXT,
                    updated_at TEXT
                );
            """)

            conn.commit()

    def execute(self, query: str, params: tuple = ()):
        """Run insert/update/delete SQL commands."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def fetch_all(self, query: str, params: tuple = ()):
        """Fetch multiple rows as list of dicts."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def fetch_one(self, query: str, params: tuple = ()):
        """Fetch single row as dict."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
