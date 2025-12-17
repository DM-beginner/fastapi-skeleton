import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)
from core.logger import setup_logging
from middlewares.logger_middleware import log_requests_middleware
from routers.v1 import example_router
from core.settings import settings
from core.database import warm_up, close_db

# 初始化日志配置
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时的逻辑（如果需要的话）
    await warm_up()
    yield
    # 应用关闭时的逻辑（如果需要的话）
    await close_db()


def register_middleware(app: FastAPI) -> None:
    # 类中间件注册
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=settings.METHODS,
        allow_headers=settings.HEADERS,
    )
    app.middleware("http")(log_requests_middleware)  # 函数中间件注册


def register_exception_handlers(app: FastAPI) -> None:
    """注册全局异常处理器"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)


def register_routes(app: FastAPI) -> None:
    prefix_version = "/v1"
    app.include_router(router=example_router.router, prefix=f"{prefix_version}")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Example APP",
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs",
    )
    register_middleware(app)
    register_exception_handlers(app)
    register_routes(app)

    return app


def run() -> None:
    try:
        import uvloop

        uvloop.install()
    except ImportError:
        print("uvloop not found, using standard asyncio loop.")

    if settings.ENV == "dev":
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            log_level="error",
            ws_ping_interval=10,
            loop="auto",
            reload=True,
        )
    else:
        uvicorn.run(
            create_app(),
            host=settings.HOST,
            port=settings.PORT,
            log_level="error",
            ws_ping_interval=10,
            loop="auto",
        )


app = create_app()

if __name__ == "__main__":
    # gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9000 app_loader:app
    run()
