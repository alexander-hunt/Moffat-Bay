"""Environment-based application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Default configuration shared by local and deployed environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in {"1", "true", "yes"}

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "moffat_bay")
    MYSQL_USER = os.getenv("MYSQL_USER", "moffat_app")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

