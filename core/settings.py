from typing import Literal, List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类
    - 默认值为开发环境配置
    - 生产环境通过 CI/CD 注入环境变量覆盖

    优先级顺序:
    1. 环境变量（系统级）
    2. .env 文件（项目级）
    3. 类中的默认值（代码级）
    """

    # 环境标识
    ENV: Literal["dev", "prod"] = "dev"

    # 应用信息
    VERSION: str = "0.1.0"

    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 5683

    # 数据库配置
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:password@localhost:5432/your_database_name"
    )

    # 日志配置
    LOG_PATH: str = "logs/your_app_name.log"
    ROTATION: str = "1 day"
    RETENTION: str = "10 days"

    # CORS 配置
    ORIGINS: List[str] = ["*"]
    METHODS: List[str] = ["*"]
    HEADERS: List[str] = ["*"]

    # Redis 配置（按需启用）
    # REDIS_HOST: str = "localhost"
    # REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        env_file=".env",  # 从 .env 文件读取
        env_file_encoding="utf-8",
        case_sensitive=True,  # 环境变量区分大小写
        extra="ignore",  # 忽略额外的环境变量
    )


settings = Settings()
