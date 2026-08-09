from apscheduler.schedulers.background import BackgroundScheduler

from discovery import discover_topics
from pipeline import process_topics


AGENT_ID = "e3345157-eeb8-4b40-9a46-1b0900db5573"


def autonomous_cycle():

    print("\n================================")
    print("AUTONOMOUS CYCLE STARTED")
    print("================================\n")

    try:

        # Step 1 — Discover new topics
        topics = discover_topics(AGENT_ID)

        print(
            f"New topics discovered: {len(topics)}"
        )

        # Step 2 — Run editorial pipeline
        process_topics()

        print("\n================================")
        print("AUTONOMOUS CYCLE COMPLETE")
        print("================================\n")

    except Exception as error:

        print(
            f"Autonomous cycle error: {error}"
        )


scheduler = BackgroundScheduler()

# Run once every 30 minutes
scheduler.add_job(
    autonomous_cycle,
    "interval",
    minutes=30,
    id="ai_agent_cycle",
    replace_existing=True
)


def start_scheduler():

    scheduler.start()

    print(
        "Autonomous scheduler started."
    )