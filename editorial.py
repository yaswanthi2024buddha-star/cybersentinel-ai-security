import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is not set in .env"
    )


# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


def evaluate_topic(
    persona_name,
    persona_domain,
    title,
    summary
):

    prompt = f"""
You are {persona_name}, an autonomous AI technology persona.

Your domain is:
{persona_domain}

You discover AI and technology news and decide
whether each topic deserves publication.

Your editorial standards:

1. The topic must strongly relate to AI or technology.
2. It should be genuinely interesting, useful, or important.
3. It should have current relevance.
4. Reject generic promotional content.
5. Reject repetitive topics.
6. Prefer meaningful technical developments.
7. Be selective.
8. Do NOT publish every topic.

Evaluate this topic:

TITLE:
{title}

SUMMARY:
{summary}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "decision": "publish",
    "score": 0,
    "relevance": 0,
    "security_risk": 0,
    "technical_impact": 0,
    "urgency": 0,
    "confidence": 0,
    "reason": "Why this topic was selected or rejected",
    "why_now": "Why this topic is or is not relevant now"
}}

Rules:

The decision must be either:
"publish"
or
"reject"

The score must be between 0 and 100.

"relevance" must be between 0 and 100.

"security_risk" must be between 0 and 100.

"technical_impact" must be between 0 and 100.

"urgency" must be between 0 and 100.

"confidence" must be between 0 and 100.

The score represents the overall editorial value of the topic.

The relevance score represents how strongly the topic relates
to the persona's domain.

The security_risk score represents the potential security
impact of the topic.

The technical_impact score represents the significance of
the underlying technical development.

The urgency score represents how important the topic is
right now.

The confidence score represents how confident you are
in your assessment.

Give a short factual reason for the decision.

Explain why the topic matters now in "why_now".

Do not include Markdown.

Do not include code fences.

Return JSON only.
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    response_text = response.choices[0].message.content

    return json.loads(response_text)


# Test editorial judgment
if __name__ == "__main__":

    result = evaluate_topic(
        "CyberSentinel",
        "AI Security",
        "A company launches a new AI themed coffee mug",
        "A company has released a coffee mug with an AI logo."
    )

    print("\n================================")
    print("EDITORIAL DECISION")
    print("================================\n")

    print(
        json.dumps(
            result,
            indent=4
        )
    )