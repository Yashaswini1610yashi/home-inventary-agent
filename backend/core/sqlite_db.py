import sqlite3

class SQLiteDB:
    """Simple synchronous SQLite setup class."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_tables()

    def connect(self):
        """Create connection to DB"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_tables(self):
        """Create only the inventory table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # --- Only Inventory Table ---
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT,
                    cat_name TEXT,
                    item_status TEXT,
                    comment TEXT,
                    username TEXT,
                    last_updated_at TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
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


# Initialize DB with only inventory
memory_db = SQLiteDB("Home.db")
