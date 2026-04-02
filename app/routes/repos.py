from fastapi import APIRouter, Query

from app.github_client import github_get
from app.models.schemas import RepositoryResponse

router = APIRouter(prefix="/repos", tags=["Repositories"])


@router.get("/", response_model=list[RepositoryResponse])
async def list_repositories(
    username: str = Query(..., description="GitHub username or organisation name"),
    per_page: int = Query(30, ge=1, le=100, description="Results per page"),
    page: int = Query(1, ge=1, description="Page number"),
):
    """Fetch public repositories for a given GitHub user or organisation."""
    data = await github_get(
        f"/users/{username}/repos",
        params={"per_page": per_page, "page": page, "sort": "updated"},
    )
    return [RepositoryResponse(**repo) for repo in data]
