from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import supabase

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