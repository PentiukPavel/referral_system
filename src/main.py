from fastapi import FastAPI
from logs.log_middleware import LoggingMiddleware

from api.routers import v1_main_router
from utils.lifespan import lifespan


app = FastAPI(
    title="Referral System",
    summary="API для реферальной системы.",
    lifespan=lifespan,
)

app.middleware("http")(LoggingMiddleware())

app.include_router(v1_main_router)
