from pydantic import BaseModel

class RepoSummary(BaseModel):
    name: str
    stars: int
    language: str | None
    url: str
    updated_at: str

class UserStats(BaseModel):
    name: str | None
    username: str
    avatar_url: str
    bio: str | None
    followers: int
    public_repos: int
    top_repos: list[RepoSummary]
    top_languages: dict[str, float]
    weekly_commits: list[int]