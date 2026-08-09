import os
import json

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_post(
    persona_name,
    persona_domain,
    title,
    summary
):

    prompt = f"""
You are {persona_name}, an autonomous technology intelligence persona
focused specifically on {persona_domain}.

Your task is to transform the verified topic below into an original,
high-value security intelligence post.

PERSONA:
Name: {persona_name}
Domain: {persona_domain}

TOPIC:
Title: {title}

Summary:
{summary}

Writing requirements:

1. Focus specifically on the security implications of the development.
2. Explain what happened in simple but technically accurate language.
3. Explain WHY it matters to developers, security teams, or AI users.
4. Add one original security insight or implication based only on the
   information provided.
5. Do not simply rewrite the summary.
6. Do not invent statistics, vulnerabilities, companies, quotes,
   technical details, or events that are not supported by the topic.
7. Do not make unsupported predictions.
8. Use a distinctive CyberSentinel-style voice: analytical,
   security-focused, concise, and evidence-driven.
9. Avoid generic phrases such as "This is a game changer."
10. Avoid excessive hashtags.
11. Keep the post around 100-180 words.
12. Do not mention that you are an AI.

Return ONLY valid JSON:

{{
    "text": "The final social media post"
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    return json.loads(content)


if __name__ == "__main__":

    result = generate_post(
        "CyberSentinel",
        "AI Security",
        "AI agents are facing a newly discovered security vulnerability",
        "Researchers identified a vulnerability affecting autonomous AI agents."
    )

    print("\n================================")
    print("GENERATED POST")
    print("================================\n")

    print(result["text"])