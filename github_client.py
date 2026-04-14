import httpx
import os

BASE = "https://api.github.com"

def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["authorization"] = f"Bearer {token}"
    return headers


async def get_user(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE}/users/{username}", 
            headers=get_headers()
        )
        if response.status_code == 404:
            return {"error": "User not found"}
        if response.status_code == 403:
            return {"error": "Rate limit hit - add a GitHub token to .env"}
        response.raise_for_status()
        return response.json()
    

async def get_repos(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE}/users/{username}/repos",
            headers=get_headers(),
            params={"per_page": 30, "sort": "update"}
        )
        if response.status_code == 404:
            return {"error": "User not found"}
        response.raise_for_status()
        return response.json()
    
async def get_events(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE}/users/{username}/events/public",
            headers = get_headers(),
            params = {"per_page": 100}
        )
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()