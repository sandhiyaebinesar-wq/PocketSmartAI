import json

from google import genai

from Backend.settings import get_settings


def get_gemini_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        return None

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def get_gemini_recommendation(planner, data):
    client = get_gemini_client()

    if client is None:
        return None

    settings = get_settings()

    prompt = f"""
You are PocketSmart AI, a smart budget recommendation assistant.

Planner: {planner}

User information:
{json.dumps(data, indent=2)}

Give practical recommendations based on the user's budget.

Return ONLY valid JSON in this format:

{{
    "planner": "{planner}",
    "summary": "short summary",
    "items": [
        {{
            "name": "product or recommendation name",
            "category": "category",
            "price": 0,
            "platform": "Amazon",
            "reason": "short reason"
        }}
    ]
}}

Do not add markdown.
Do not add explanations outside JSON.
"""

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)

    except Exception:
        return None