from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes import repos, issues, commits

app = FastAPI(
    title="GitHub Cloud Connector",
    description="A REST API connector that authenticates with GitHub and exposes endpoints for repositories, issues, and commits.",
    version="1.0.0",
)

app.include_router(repos.router)
app.include_router(issues.router)
app.include_router(commits.router)


@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint to verify the connector is running."""
    return {"status": "healthy", "service": "GitHub Cloud Connector"}
