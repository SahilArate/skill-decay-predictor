from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import supabase
from schemas import SkillCreate, PracticeEventCreate
from decay import calculate_retention

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
    now = datetime.now(timezone.utc).isoformat()

    event_response = supabase.table("practice_events").insert({
        "skill_id": event.skill_id,
        "source": event.source,
        "practiced_at": now,
        "intensity": event.intensity,
    }).execute()

    supabase.table("skills").update({
        "last_practiced_at": now
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