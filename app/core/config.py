import secrets
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union
import os


class Settings(BaseSettings):
    # API 配置
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "2d383dfce524f91dcd4fd0bcbcaac"

    # Token 过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # CORS 配置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 数据库地址
    Mysql_ip = "10.10.10.10"
    Mysql_port = "3306"
    Mysql_pwd = "pwd"
    table_name = "test_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = (
        "mysql+pymysql://root:"
        + Mysql_pwd
        + "@"
        + Mysql_ip
        + ":"
        + Mysql_port
        + "/"
        + table_name
        + "?charset=utf8mb4"
    )

    # Elasticsearch 配置
    ES_ip = "10.10.10.10"
    ES_port = "9002"
    ES_DATABASE_URI: str = "http://{0}:{1}".format(ES_ip, ES_port)  # 替代 es_ip

    # 用户配置
    USERS_OPEN_REGISTRATION: bool = True
    TEST_USER = "test"
    TEST_USER_PASSWORD = "test@iie"
    FIRST_SUPERUSER = "root"
    FIRST_SUPERUSER_PASSWORD = "root@iie"
    # 项目名称
    PROJECT_NAME: str = "Project-Api-Demo"

    # home 目录
    home_dir = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )

    class Config:
        case_sensitive = True

    index_crypted_message = "crypted_message"


settings = Settings()
