from fastapi import APIRouter

from core.database import SessionDep
from schemas.example_schema import Example
from repos import example_repo
from loguru import logger

router = APIRouter(tags=["example"], prefix="/example")


@router.get("/example", response_model=list[Example])
async def get_example(db: SessionDep):
    """获取示例数据"""
    logger.info("get_example")
    return await example_repo.get_example(db)
