from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import db
from .config import get_settings
from .migrate import migrate
from .routers import (
    auth as auth_router,
    cases,
    chat,
    citations,
    documents,
    endeavor,
    eval as eval_router,
    evidence,
    forms,
    ingest,
    jobs,
    recommenders,
)


_KNOWN_DEFAULT_SECRETS = {"change-me", "selfhost-dev-secret-change-me", ""}


@asynccontextmanager
async def lifespan(app: FastAPI):
    if get_settings().secret_key in _KNOWN_DEFAULT_SECRETS:
        import logging
        logging.getLogger("uvicorn.error").warning(
            "SECRET_KEY is a shipped default — anyone who can reach this "
            "server can forge login tokens. Generate one: "
            "python3 -c \"import secrets; print(secrets.token_hex(32))\" "
            "and set it in .env. Safe only on localhost."
        )
    await migrate()
    yield
    await db.close_pool()


app = FastAPI(
    title="OpenNIW API",
    description=(
        "Open-source AI-assisted EB-2 NIW petition preparation. "
        "Not a law firm; not legal advice."
    ),
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    auth_router.router, eval_router.router, cases.router, evidence.router,
    documents.router, recommenders.router, chat.router, ingest.router,
    forms.router, jobs.router, citations.router, endeavor.router,
):
    app.include_router(router)


@app.get("/health")
async def health() -> dict:
    return {"ok": True}
