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

    # AGENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # POSTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL,
            rationale TEXT NOT NULL,
            sources TEXT NOT NULL
        )
    """)

    # TOPICS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            summary TEXT,
            discovered_at TEXT,
            decision TEXT,
            score REAL,
            relevance REAL,
            security_risk REAL,
            technical_impact REAL,
            urgency REAL,
            confidence REAL,
            priority TEXT,
            why_now TEXT
        )
    """)

    # Make sure the CyberSentinel agent exists
    cursor.execute("""
        INSERT OR IGNORE INTO agents
        (id, name, domain)
        VALUES (?, ?, ?)
    """, (
        AGENT_ID,
        "CyberSentinel",
        "AI Security"
    ))

    connection.commit()
    connection.close()

    print("Database initialized successfully.")


def topic_exists(url):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM topics WHERE url = ?",
        (url,)
    )

    topic = cursor.fetchone()

    connection.close()

    return topic is not None


def save_topic(
    agent_id,
    title,
    url,
    summary,
    discovered_at
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO topics (
            agent_id,
            title,
            url,
            summary,
            discovered_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        agent_id,
        title,
        url,
        summary,
        discovered_at
    ))

    connection.commit()
    connection.close()


def get_pending_topics(agent_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM topics
        WHERE agent_id = ?
        AND decision IS NULL
        ORDER BY id ASC
    """, (agent_id,))

    topics = cursor.fetchall()

    connection.close()

    return topics


def update_topic_decision(
    topic_id,
    decision,
    score
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE topics
        SET
            decision = ?,
            score = ?
        WHERE id = ?
    """, (
        decision,
        score,
        topic_id
    ))

    connection.commit()
    connection.close()


def get_all_topics(agent_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM topics
        WHERE agent_id = ?
        ORDER BY id ASC
    """, (agent_id,))

    topics = cursor.fetchall()

    connection.close()

    return topics


def save_post(
    post_id,
    agent_id,
    created_at,
    text,
    rationale,
    sources
):
    connection = get_connection()
    cursor = connection.cursor()

    if isinstance(sources, (list, dict)):
        sources = json.dumps(sources)

    cursor.execute("""
        INSERT INTO posts (
            id,
            agent_id,
            created_at,
            text,
            rationale,
            sources
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        post_id,
        agent_id,
        created_at,
        text,
        rationale,
        sources
    ))

    connection.commit()
    connection.close()


def get_posts(agent_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM posts
        WHERE agent_id = ?
        ORDER BY created_at DESC
    """, (agent_id,))

    posts = cursor.fetchall()

    connection.close()

    return posts


def get_agent(agent_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM agents
        WHERE id = ?
    """, (agent_id,))

    agent = cursor.fetchone()

    connection.close()

    return agent


def update_topic_analysis(
    topic_id,
    decision,
    score,
    relevance,
    security_risk,
    technical_impact,
    urgency,
    confidence,
    priority,
    why_now
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE topics
        SET
            decision = ?,
            score = ?,
            relevance = ?,
            security_risk = ?,
            technical_impact = ?,
            urgency = ?,
            confidence = ?,
            priority = ?,
            why_now = ?
        WHERE id = ?
    """, (
        decision,
        score,
        relevance,
        security_risk,
        technical_impact,
        urgency,
        confidence,
        priority,
        why_now,
        topic_id
    ))

    connection.commit()
    connection.close()


def reset_topic_decisions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE topics
        SET
            decision = NULL,
            score = NULL,
            relevance = NULL,
            security_risk = NULL,
            technical_impact = NULL,
            urgency = NULL,
            confidence = NULL,
            priority = NULL,
            why_now = NULL
    """)

    connection.commit()
    connection.close()

    print("All topic decisions have been reset.")
