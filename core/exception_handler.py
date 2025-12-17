from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger
import traceback

from core.settings import settings


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理 FastAPI 的 HTTPException"""
    logger.warning(
        f"HTTPException: {exc.status_code} - {exc.detail} | "
        f"Path: {request.method} {request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
            },
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求参数验证错误（Pydantic）"""
    errors = exc.errors()
    logger.warning(
        f"Validation error: {errors} | " f"Path: {request.method} {request.url.path}"
    )

    # 格式化验证错误信息
    error_messages = []
    for error in errors:
        loc = " -> ".join(str(x) for x in error["loc"])
        error_messages.append(f"{loc}: {error['msg']}")

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "请求参数验证失败",
                "details": error_messages,
            },
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """处理所有未捕获的异常"""
    # 记录完整的堆栈信息
    logger.error(
        f"Unhandled exception: {type(exc).__name__}: {str(exc)} | "
        f"Path: {request.method} {request.url.path}\n"
        f"Traceback: {traceback.format_exc()}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "服务器内部错误",
                # 生产环境建议隐藏详细错误信息
                "detail": str(exc) if settings.ENV == "dev" else None,
            },
        },
    )
