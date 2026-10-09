from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.clones import router as clones_router
from app.api.environments import router as environments_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Ephemeral Production-Faithful Test Environments for Coding Agents"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clones_router, prefix=settings.API_V1_STR)
app.include_router(environments_router, prefix=settings.API_V1_STR)

@app.get("/healthz")
async def healthcheck():
    return {
        "status": "ok",
        "service": "forgelab-runtime",
        "version": settings.VERSION,
        "cloner": "cow-sqlite-active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8004, reload=True)
