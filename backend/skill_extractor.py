import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

EXTRACTION_PROMPT = """You are analyzing a Git commit message to identify which technical skill was practiced.

Commit message: "{message}"

Respond with ONLY a JSON object in this exact format, nothing else:
{{"skill_name": "short skill name, e.g. 'FastAPI', 'React', 'SQL', 'Database Design'", "category": "Programming, Language, Design, or Other", "confidence": a number from 0 to 1}}

If the commit message is too vague to determine a skill (e.g. "fix typo", "update readme"), respond with:
{{"skill_name": null, "category": null, "confidence": 0}}
"""


def extract_skill_from_commit(commit_message: str) -> dict:
    """
    Sends a commit message to the LLM and asks it to classify
    which skill was likely being practiced.
    """
    prompt = EXTRACTION_PROMPT.format(message=commit_message)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
        reasoning_effort="low",
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        parsed = {"skill_name": None, "category": None, "confidence": 0}

    return parsed