import sqlite3

DATABASE_NAME = "agent.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Agents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL,
            rationale TEXT NOT NULL,
            sources TEXT NOT NULL,
            FOREIGN KEY (agent_id) REFERENCES agents(id)
        )
    """)

    # Topics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        summary TEXT,
        discovered_at TEXT NOT NULL,
        decision TEXT,
        score REAL,
        FOREIGN KEY (agent_id) REFERENCES agents(id)
    )
""")

    # Add new AI risk-analysis columns
    new_columns = [
        ("summary", "TEXT"),
        ("relevance", "REAL"),
        ("security_risk", "REAL"),
        ("technical_impact", "REAL"),
        ("urgency", "REAL"),
        ("confidence", "REAL"),
        ("priority", "TEXT"),
        ("why_now", "TEXT")
    ]

    for column_name, column_type in new_columns:

        try:
            cursor.execute(
                f"ALTER TABLE topics ADD COLUMN {column_name} {column_type}"
            )

        except sqlite3.OperationalError:
            # Column already exists
            pass

    connection.commit()
    connection.close()


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
        SET decision = ?,
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