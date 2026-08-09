 import sqlite3
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "database.db"

AGENT_ID = "e3345157-eeb8-4b40-9a46-1b0900db5573"


def get_connection():
    connection = sqlite3.connect(
        DATABASE_FILE,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------
    # AGENTS
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------
    # POSTS
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL,
            rationale TEXT,
            sources TEXT
        )
    """)

    # --------------------------------------------------
    # TOPICS
    # --------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT,
            title TEXT,
            url TEXT,
            decision TEXT,
            score INTEGER,
            relevance INTEGER,
            security_risk INTEGER,
            technical_impact INTEGER,
            urgency INTEGER,
            confidence INTEGER,
            priority TEXT,
            why_now TEXT
        )
    """
