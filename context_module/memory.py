import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "memory.db"


def _get_connection():
    return sqlite3.connect(DB_PATH)


def init_memory():
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_message(user_id: str, role: str, content: str):

    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversation(user_id, role, content)
        VALUES (?, ?, ?)
        """,
        (user_id, role, content)
    )

    conn.commit()
    conn.close()


def get_conversation_context(
    user_id: str,
    max_messages: int = 6
):

    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM conversation
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, max_messages)
    )

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in rows
    ]


def clear_memory(user_id: str):

    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM conversation
        WHERE user_id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()


init_memory()