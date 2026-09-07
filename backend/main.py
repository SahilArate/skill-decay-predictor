from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import supabase
from schemas import SkillCreate, PracticeEventCreate
from decay import calculate_retention, update_stability
from github_client import fetch_recent_commits
from skill_extractor import extract_skill_from_commit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Skill Decay Predictor API is running"}


@app.get("/skills")
def get_skills():
    response = supabase.table("skills").select("*").execute()
    return response.data


@app.post("/skills")
def create_skill(skill: SkillCreate):
    response = supabase.table("skills").insert({
        "name": skill.name,
        "category": skill.category,
    }).execute()
    return response.data


@app.post("/practice-events")
def create_practice_event(event: PracticeEventCreate):
    now = datetime.now(timezone.utc)

    skill_response = supabase.table("skills").select("*").eq("id", event.skill_id).execute()
    if not skill_response.data:
        return {"error": "Skill not found"}

    skill = skill_response.data[0]

    if skill["last_practiced_at"]:
        last_practiced = datetime.fromisoformat(skill["last_practiced_at"])
        days_since_last = (now - last_practiced).total_seconds() / 86400
    else:
        days_since_last = 0

    new_stability = update_stability(
        current_stability=skill["stability"],
        intensity=event.intensity,
        days_since_last_practice=days_since_last,
    )

    event_response = supabase.table("practice_events").insert({
        "skill_id": event.skill_id,
        "source": event.source,
        "practiced_at": now.isoformat(),
        "intensity": event.intensity,
    }).execute()

    supabase.table("skills").update({
        "last_practiced_at": now.isoformat(),
        "stability": new_stability,
    }).eq("id", event.skill_id).execute()

    return event_response.data

@app.get("/skills/decay-status")
def get_skills_with_decay():
    response = supabase.table("skills").select("*").execute()
    skills = response.data

    result = []
    for skill in skills:
        retention = calculate_retention(
            skill["last_practiced_at"],
            skill["stability"]
        )
        result.append({
            **skill,
            "retention": retention,
        })

    return result

@app.post("/sync-github")
def sync_github_commits():
    commits = fetch_recent_commits(limit=10)
    results = []

    for commit in commits:
        extracted = extract_skill_from_commit(commit["message"])

        if not extracted.get("skill_name"):
            continue

        skill_name = extracted["skill_name"]
        category = extracted.get("category")

        existing = supabase.table("skills").select("*").ilike("name", skill_name).execute()

        if existing.data:
            skill = existing.data[0]
        else:
            created = supabase.table("skills").insert({
                "name": skill_name,
                "category": category,
            }).execute()
            skill = created.data[0]

        now = datetime.now(timezone.utc)

        if skill["last_practiced_at"]:
            last_practiced = datetime.fromisoformat(skill["last_practiced_at"])
            days_since_last = (now - last_practiced).total_seconds() / 86400
        else:
            days_since_last = 0

        new_stability = update_stability(
            current_stability=skill["stability"],
            intensity=extracted.get("confidence", 0.5),
            days_since_last_practice=days_since_last,
        )

        supabase.table("practice_events").insert({
            "skill_id": skill["id"],
            "source": "github",
            "practiced_at": commit["date"],
            "intensity": extracted.get("confidence", 0.5),
            "raw_reference": commit["url"],
        }).execute()

        supabase.table("skills").update({
            "last_practiced_at": now.isoformat(),
            "stability": new_stability,
        }).eq("id", skill["id"]).execute()

        results.append({
            "commit": commit["message"],
            "detected_skill": skill_name,
            "category": category,
        })

    return {"processed": len(results), "results": results}