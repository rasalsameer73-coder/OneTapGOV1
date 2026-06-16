import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.lifespan import lifespan
import importlib
import logging

_log = logging.getLogger("app.routers")

ROUTERS = [
    ("app.modules.auth.routes", "/api/v1/auth", ["Authentication"]),
    ("app.modules.profile.routes", "/api/v1/profile", ["Profile"]),
    ("app.modules.education.routes", "/api/v1/education", ["Education"]),
    ("app.modules.women.routes", "/api/v1/women", ["Women Welfare"]),
    ("app.modules.agriculture.routes", "/api/v1/agriculture", ["Agriculture"]),
    ("app.modules.schemes.routes", "/api/v1/schemes", ["Schemes"]),
    ("app.modules.eligibility.routes", "/api/v1/eligibility", ["Eligibility"]),
    ("app.modules.documents.routes", "/api/v1/documents", ["Documents"]),
    ("app.modules.recommendation.routes", "/api/v1/recommendations", ["Recommendations"]),
    ("app.modules.user_documents.routes", "/api/v1/user-documents", ["User Documents"]),
    ("app.modules.readiness.routes", "/api/v1/readiness", ["Readiness"]),
    ("app.modules.assistant.routes", "/api/v1/assistant", ["AI Assistant"]),
    ("app.modules.admin.routes", "/api/v1/admin", ["Admin"]),
]


# Load environment: prefer backend/.env if present, fall back to app/.env
backend_env = Path(__file__).parents[1] / "backend" / ".env"
if backend_env.exists():
    load_dotenv(dotenv_path=backend_env)
else:
    load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

# If key envs still missing, try loading with utf-16 encoding (partner formats)
if not os.getenv("SUPABASE_URL") and not os.getenv("NEXT_PUBLIC_SUPABASE_URL"):
    if backend_env.exists():
        load_dotenv(dotenv_path=backend_env, encoding="utf-16")
    else:
        load_dotenv(dotenv_path=Path(__file__).with_name(".env"), encoding="utf-16")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

# Add CORS middleware (allows localhost origins by regex)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"http://(localhost|127\\.0\\.0\\.1)(:\\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount backend chat router only when Supabase envs are available to avoid import-time failures
if os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL"):
    try:
        from backend.api import chat

        app.include_router(chat.router)
    except Exception:
        # If importing backend chat fails, log and continue without it.
        import logging

        logging.getLogger("app").exception("Failed to include backend.chat router; continuing without Supabase-backed routes.")
else:
    import logging

    logging.getLogger("app").info("SUPABASE envs not found; skipping backend.chat router mount.")


# Dynamically include core API routers, falling back to backend package when needed
for module_path, prefix, tags in ROUTERS:
    router = None
    try:
        mod = importlib.import_module(module_path)
        router = getattr(mod, "router", None)
    except Exception:
        try:
            backend_module_path = module_path.replace("app.", "backend.app.")
            mod = importlib.import_module(backend_module_path)
            router = getattr(mod, "router", None)
        except Exception:
            _log.exception("Failed to import router module %s or its backend fallback", module_path)

    if router is None:
        _log.info("Router for %s not found; skipping", module_path)
        continue

    app.include_router(router, prefix=prefix, tags=tags)


@app.get("/")
async def root():
    return {"message": "OneTapGOV Backend Running"}