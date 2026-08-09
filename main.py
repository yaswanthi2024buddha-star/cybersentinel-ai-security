from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from database import (
    initialize_database,
    get_connection,
    get_posts,
    get_agent
)

from scheduler import start_scheduler


app = FastAPI(
    title="Autonomous AI Creator",
    description="Autonomous AI Security content agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


AGENT_ID = "e3345157-eeb8-4b40-9a46-1b0900db5573"


# Dashboard file location
BASE_DIR = Path(__file__).resolve().parent
DASHBOARD_FILE = BASE_DIR / "dashboard.html"


# Initialize database when API starts
initialize_database()


# Start autonomous background scheduler
start_scheduler()


# ---------------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------------

@app.get("/")
def home():
    return FileResponse(DASHBOARD_FILE)


# ---------------------------------------------------------
# AGENT INFORMATION
# ---------------------------------------------------------

@app.get("/api/agent")
def agent_info():

    agent = get_agent(AGENT_ID)

    if agent is None:

        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    return {
        "id": agent["id"],
        "name": agent["name"],
        "domain": agent["domain"],
        "createdAt": agent["created_at"]
    }


# ---------------------------------------------------------
# AGENT FEED
# ---------------------------------------------------------

@app.get("/api/agent/feed")
def agent_feed():

    posts = get_posts(AGENT_ID)

    return {
        "agentId": AGENT_ID,
        "agentName": "CyberSentinel",
        "domain": "AI Security",
        "posts": [
            {
                "id": post["id"],
                "createdAt": post["created_at"],
                "text": post["text"],
                "rationale": post["rationale"],
                "sources": post["sources"]
            }
            for post in posts
        ]
    }


# ---------------------------------------------------------
# PUBLISHED POSTS
# ---------------------------------------------------------

@app.get("/api/agent/posts")
def agent_posts():

    posts = get_posts(AGENT_ID)

    return [
        {
            "id": post["id"],
            "createdAt": post["created_at"],
            "text": post["text"],
            "rationale": post["rationale"],
            "sources": post["sources"]
        }
        for post in posts
    ]


# ---------------------------------------------------------
# TOPICS
# ---------------------------------------------------------

@app.get("/api/agent/topics")
def agent_topics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            url,
            decision,
            score,
            relevance,
            security_risk,
            technical_impact,
            urgency,
            confidence,
            priority,
            why_now
        FROM topics
        WHERE agent_id = ?
        ORDER BY id DESC
    """, (AGENT_ID,))

    topics = cursor.fetchall()

    connection.close()

    return [
        {
            "id": topic["id"],
            "title": topic["title"],
            "url": topic["url"],
            "decision": topic["decision"],
            "score": topic["score"],
            "relevance": topic["relevance"],
            "securityRisk": topic["security_risk"],
            "technicalImpact": topic["technical_impact"],
            "urgency": topic["urgency"],
            "confidence": topic["confidence"],
            "priority": topic["priority"],
            "whyNow": topic["why_now"]
        }
        for topic in topics
    ]
