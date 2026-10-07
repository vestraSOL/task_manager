import logging
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware

from files.main.core.logging import config_logging
from files.main.config.config import get_settings
from files.main.routers.tasks import router as task_router

config_logging()
settings=get_settings()
logger=logging.getLogger("app.middleware")


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=task_router)



@app.middleware('http')
async def log_requests(request: Request, call_next)->Response:
    started_at=perf_counter()
    try:
        response: Response=await call_next(request)
    except Exception:
        duration_ms=(perf_counter() - started_at)*1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise
    duration_ms=(perf_counter() - started_at)*1000
    logger.info(
        '%s %s -> %s (%.2f ms)',
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'])













