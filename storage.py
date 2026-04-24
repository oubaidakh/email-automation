import sqlite3
import os

class Database:
    def __init__(self, db_path="processed_emails.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database and create the table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_emails (
                    email TEXT PRIMARY KEY,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def is_processed(self, email):
        """Check if an email has already been processed."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM processed_emails WHERE email = ?', (email,))
            return cursor.fetchone() is not None

    def mark_as_processed(self, email):
        """Mark an email as processed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO processed_emails (email) VALUES (?)', (email,))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Already exists
