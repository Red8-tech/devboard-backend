from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from github_client import get_user, get_repos, get_events
from dotenv import load_dotenv
from process import build_user_stats
from datetime import datetime, timedelta

cache: dict = {}
CACHE_TTL = timedelta(minutes=5)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/user/{username}")
async def user(username: str):
    profile = await get_user(username)
    repos = await get_repos(username)
    return {"profile": profile, "repos": repos}

@app.get("/stats/{username}")
async def status(username: str):
    if username in cache:
        data, cached_at = cache[username]
        if datetime.now() - cached_at < CACHE_TTL:
            return data
        
    profile = await get_user(username)
    if "error" in profile:
        return profile
    
    repos = await get_repos(username)
    events = await get_events(username)

    result = build_user_stats(profile, repos, events)
    cache[username] = (result, datetime.now())
    return result