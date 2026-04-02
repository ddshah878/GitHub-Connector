from pydantic import BaseModel, Field


# ── Request Schemas ──────────────────────────────────────────────

class CreateIssueRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=256, examples=["Bug: login page crash"])
    body: str | None = Field(None, examples=["Steps to reproduce the issue..."])
    labels: list[str] = Field(default_factory=list, examples=[["bug", "urgent"]])


# ── Response Schemas ─────────────────────────────────────────────

class RepositoryResponse(BaseModel):
    id: int
    name: str
    full_name: str
    description: str | None
    html_url: str
    language: str | None
    stargazers_count: int
    forks_count: int
    private: bool


class IssueResponse(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
    created_at: str
    body: str | None


class CommitResponse(BaseModel):
    sha: str
    message: str
    author_name: str | None
    author_date: str | None
    html_url: str


