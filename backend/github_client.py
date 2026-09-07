import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME")
GITHUB_REPO = os.environ.get("GITHUB_REPO")

BASE_URL = "https://api.github.com"


def fetch_recent_commits(limit: int = 10):
    """
    Fetches the most recent commits from the configured GitHub repo.
    Returns a simplified list of commit messages, dates, and changed files.
    """
    url = f"{BASE_URL}/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/commits"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    params = {"per_page": limit}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    commits = response.json()

    simplified = []
    for commit in commits:
        simplified.append({
            "sha": commit["sha"],
            "message": commit["commit"]["message"],
            "date": commit["commit"]["author"]["date"],
            "url": commit["html_url"],
        })

    return simplified