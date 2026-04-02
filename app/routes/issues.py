from fastapi import APIRouter, Path, Query

from app.github_client import github_get, github_post
from app.models.schemas import CreateIssueRequest, IssueResponse

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.get("/{owner}/{repo}", response_model=list[IssueResponse])
async def list_issues(
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
    state: str = Query("open", regex="^(open|closed|all)$", description="Issue state filter"),
    per_page: int = Query(30, ge=1, le=100, description="Results per page"),
    page: int = Query(1, ge=1, description="Page number"),
):
    """List issues for a specific repository."""
    data = await github_get(
        f"/repos/{owner}/{repo}/issues",
        params={"state": state, "per_page": per_page, "page": page},
    )
    return [IssueResponse(**issue) for issue in data]


@router.post("/{owner}/{repo}", response_model=IssueResponse, status_code=201)
async def create_issue(
    body: CreateIssueRequest,
    owner: str = Path(..., description="Repository owner"),
    repo: str = Path(..., description="Repository name"),
):
    """Create a new issue in a repository."""
    payload = {"title": body.title, "body": body.body, "labels": body.labels}
    data = await github_post(f"/repos/{owner}/{repo}/issues", payload)
    return IssueResponse(**data)
