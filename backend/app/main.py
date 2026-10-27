from fastapi import FastAPI

app = FastAPI(
    title="AI HelpDesk API",
    description="REST API for the AI HelpDesk project",
    version="0.1.0",
)


@app.get("/api/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ai-helpdesk-backend",
    }