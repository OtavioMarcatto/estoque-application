from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.router import router
from app.config import settings
from app.core.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[type-arg]
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan,
)

app.add_middleware(GZipMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(router)


@app.get("/", response_class=RedirectResponse)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/produtos")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Any) -> HTMLResponse:
    return templates.TemplateResponse(request, "404.html", {}, status_code=404)
