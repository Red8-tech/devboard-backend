from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from github_client import get_user, get_repos
from dotenv import load_dotenv

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