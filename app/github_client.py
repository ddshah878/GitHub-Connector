import httpx
from fastapi import HTTPException

from app.config import get_settings

GITHUB_API_TIMEOUT = 15.0


def _build_headers() -> dict[str, str]:
    settings = get_settings()
    return {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _base_url() -> str:
    return get_settings().github_api_base_url


async def github_get(endpoint: str, params: dict | None = None) -> dict | list:
    """Perform an authenticated GET request to the GitHub API."""
    url = f"{_base_url()}{endpoint}"
    async with httpx.AsyncClient(timeout=GITHUB_API_TIMEOUT) as client:
        response = await client.get(url, headers=_build_headers(), params=params)

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid or expired GitHub token.")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"GitHub resource not found: {endpoint}")
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API error: {response.text}",
        )
    return response.json()


async def github_post(endpoint: str, payload: dict) -> dict:
    """Perform an authenticated POST request to the GitHub API."""
    url = f"{_base_url()}{endpoint}"
    async with httpx.AsyncClient(timeout=GITHUB_API_TIMEOUT) as client:
        response = await client.post(url, headers=_build_headers(), json=payload)

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid or expired GitHub token.")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"GitHub resource not found: {endpoint}")
    if response.status_code == 422:
        raise HTTPException(status_code=422, detail=f"Validation failed: {response.text}")
    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API error: {response.text}",
        )
    return response.json()
