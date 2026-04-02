from fastapi import APIRouter, Path, Query

from app.github_client import github_get
from app.models.schemas import CommitResponse

router = APIRouter(prefix="/commits", tags=["Commits"])


@router.get("/{owner}/{repo}", response_model=list[CommitResponse])
async def list_commits(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    per_page: int = Query(30, ge=1, le=100, description="Results per page"),
    page: int = Query(1, ge=1, description="Page number"),
):
    """Fetch commits from a repository."""
    data = await github_get(
        f"/repos/{owner}/{repo}/commits",
        params={"per_page": per_page, "page": page},
    )
    return [
        CommitResponse(
            sha=commit["sha"],
            message=commit["commit"]["message"],
            author_name=commit["commit"]["author"]["name"] if commit["commit"]["author"] else None,
            author_date=commit["commit"]["author"]["date"] if commit["commit"]["author"] else None,
            html_url=commit["html_url"],
        )
        for commit in data
    ]
