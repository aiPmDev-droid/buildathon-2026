import os

from google import genai
from google.genai import types as genai_types

SYSTEM_PROMPT = """
You write one short, witty opening line for two people who just got matched for a
coffee chat at UCLA Anderson. You'll see their three answers (favorite spot in
LA, what they're excited about, biggest challenge). Sometimes an answer is
literally the same or very close between them; other times the answers are
worded differently but share a category or vibe underneath (e.g. sushi vs.
bagels are both food; a marathon vs. surfing are both "outdoorsy"; a case
competition vs. a dissertation defense are both "high stakes this month").

Find the most interesting connection, literal or underlying, and phrase it as
ONE punchy, upbeat sentence, like "Hey! You're both foodies!" or "Sounds like
you're both chasing a big goal this quarter." If genuinely nothing connects
them, make a lighthearted joke about how different they are instead. Always
return a line, never explain your reasoning, never use quotation marks or an
em dash, and keep it under 15 words.
""".strip()

FALLBACK_HEADLINE = "You two have nothing in common. Perfect."

_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def _format_person(label: str, person: dict) -> str:
    return (
        f"{label}: favorite spot in LA — {person.get('favorite_spot_la')}; "
        f"excited about — {person.get('excited_about')}; "
        f"biggest challenge — {person.get('biggest_challenge')}"
    )


def generate_witty_headline(person: dict, partner: dict) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return FALLBACK_HEADLINE

    try:
        client = genai.Client(api_key=api_key)
        prompt = (
            f"{_format_person('Person A', person)}\n"
            f"{_format_person('Person B', partner)}"
        )
        response = client.models.generate_content(
            model=_MODEL,
            contents=[
                genai_types.Content(role="user", parts=[genai_types.Part(text=SYSTEM_PROMPT)]),
                genai_types.Content(role="user", parts=[genai_types.Part(text=prompt)]),
            ],
            config=genai_types.GenerateContentConfig(
                temperature=0.9,
                max_output_tokens=100,
                # This is a one-line quip, not a reasoning task — thinking tokens
                # would otherwise eat the whole output budget on Gemini 2.5.
                thinking_config=genai_types.ThinkingConfig(thinking_budget=0),
            ),
        )
        line = (response.text or "").strip().strip('"').strip()
        return line or FALLBACK_HEADLINE
    except Exception:
        return FALLBACK_HEADLINE
