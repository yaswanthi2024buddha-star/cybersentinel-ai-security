from datetime import datetime, timezone
import uuid

from database import (
    initialize_database,
    get_pending_topics,
    update_topic_decision,
    update_topic_analysis,
    save_post
)

from editorial import evaluate_topic
from writer import generate_post


AGENT_ID = "e3345157-eeb8-4b40-9a46-1b0900db5573"

PERSONA_NAME = "CyberSentinel"

PERSONA_DOMAIN = "AI Security"


def calculate_priority(
    score,
    security_risk,
    technical_impact,
    urgency
):

    average_score = (
        score
        + security_risk
        + technical_impact
        + urgency
    ) / 4

    if average_score >= 80:
        return "critical"

    elif average_score >= 60:
        return "high"

    elif average_score >= 40:
        return "medium"

    else:
        return "low"


def process_topics():

    initialize_database()

    topics = get_pending_topics(AGENT_ID)

    print("\n================================")
    print("AUTONOMOUS AI PIPELINE")
    print("================================\n")

    print(
        f"Pending topics: {len(topics)}\n"
    )

    published = 0
    rejected = 0

    for topic in topics:

        print("TITLE:")
        print(topic["title"])

        try:

            # --------------------------------
            # STEP 1 — Editorial evaluation
            # --------------------------------

            result = evaluate_topic(
                PERSONA_NAME,
                PERSONA_DOMAIN,
                topic["title"],
                topic["summary"]
            )

            decision = result.get(
                "decision",
                "reject"
            )

            score = result.get(
                "score",
                0
            )

            relevance = result.get(
                "relevance",
                0
            )

            security_risk = result.get(
                "security_risk",
                0
            )

            technical_impact = result.get(
                "technical_impact",
                0
            )

            urgency = result.get(
                "urgency",
                0
            )

            confidence = result.get(
                "confidence",
                0
            )

            reason = result.get(
                "reason",
                ""
            )

            why_now = result.get(
                "why_now",
                ""
            )

            # --------------------------------
            # STEP 2 — Calculate priority
            # --------------------------------

            priority = calculate_priority(
                score,
                security_risk,
                technical_impact,
                urgency
            )

            print(
                f"\nEditorial decision: {decision}"
            )

            print(
                f"Overall score: {score}"
            )

            print(
                f"Relevance: {relevance}"
            )

            print(
                f"Security risk: {security_risk}"
            )

            print(
                f"Technical impact: {technical_impact}"
            )

            print(
                f"Urgency: {urgency}"
            )

            print(
                f"Confidence: {confidence}"
            )

            print(
                f"Priority: {priority}"
            )

            print(
                f"Reason: {reason}"
            )

            print(
                f"Why now: {why_now}"
            )

            # --------------------------------
            # STEP 3 — Save complete analysis
            # --------------------------------

            update_topic_analysis(
                topic["id"],
                decision,
                score,
                relevance,
                security_risk,
                technical_impact,
                urgency,
                confidence,
                priority,
                why_now
            )

            # --------------------------------
            # STEP 4 — Reject
            # --------------------------------

            if decision != "publish":

                rejected += 1

                print(
                    "\nTopic rejected."
                )

                print(
                    "\n" + "-" * 60
                )

                continue

            # --------------------------------
            # STEP 5 — Generate post
            # --------------------------------

            print(
                "\nGenerating post..."
            )

            generated = generate_post(
                PERSONA_NAME,
                PERSONA_DOMAIN,
                topic["title"],
                topic["summary"]
            )

            post_text = generated["text"]

            # --------------------------------
            # STEP 6 — Save post
            # --------------------------------

            post_id = str(
                uuid.uuid4()
            )

            created_at = datetime.now(
                timezone.utc
            ).isoformat()

            save_post(
                post_id,
                AGENT_ID,
                created_at,
                post_text,
                reason,
                topic["url"]
            )

            published += 1

            print(
                "\nGENERATED POST:"
            )

            print(
                "------------------------------"
            )

            print(post_text)

            print(
                "------------------------------"
            )

            print(
                "\nPost saved to database."
            )

        except Exception as error:

            print(
                f"\nError processing topic: {error}"
            )

        print(
            "\n" + "-" * 60
        )

    print(
        "\n================================"
    )

    print(
        "PIPELINE COMPLETE"
    )

    print(
        "================================"
    )

    print(
        f"Published: {published}"
    )

    print(
        f"Rejected: {rejected}"
    )


if __name__ == "__main__":

    process_topics()