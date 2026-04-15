from models import RepoSummary, UserStats
from collections import Counter
import datetime


def compute_language_breakdown(repos: list) -> dict[str, float]:
    languages = [r["language"] for r in repos if r.get("language")]
    if not languages:
        return {}
    counts = Counter(languages)
    total = sum(counts.values())
    return {lang: round((count/total) * 100, 1) for lang, count in counts.most_common(6)}


def get_top_repos(repos: list) -> list[RepoSummary]:
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return [
        RepoSummary(
            name=r["name"],
            stars=r["stargazers_count"],
            language=r.get("language"),
            url=r["html_url"],
            updated_at=r["updated_at"]
        )
        for r in sorted_repos[:5]
    ]


def compute_weekly_commits(events: list) -> list[int]:
    now = datetime.datetime.now(datetime.timezone.utc)
    weeks = [0] * 12
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        created = datetime.datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
        delta_days = (now - created).days
        week_index = delta_days // 7
        if 0 <= week_index < 12:
            commits = event.get("payload", {}).get("size", 1)
            weeks[week_index] += commits
    return list(reversed(weeks))


def build_user_stats(profile: dict, repos: list, events: list) -> UserStats:
    return UserStats(
        name=profile.get("name"),
        username=profile["login"],
        avatar_url=profile["avatar_url"],
        bio=profile.get("bio"),
        followers=profile["followers"],
        public_repos=profile["public_repos"],
        top_repos=get_top_repos(repos),
        top_languages=compute_language_breakdown(repos),
        weekly_commits=compute_weekly_commits(events)
    )
