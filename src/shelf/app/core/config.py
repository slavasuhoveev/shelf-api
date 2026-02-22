"""Application configuration settings.

Provides access to environment variables and
application-level configuration values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, computed_field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ----------------------------
    # Database configuration
    # ----------------------------
    POSTGRES_USER: str = "shelf_user"
    POSTGRES_PASSWORD: str = "shelf"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "shelf_db"

    # ----------------------------
    # JWT / Auth configuration
    # ----------------------------
    AUTH_JWKS_URL: HttpUrl
    JWT_ISSUER: str
    JWT_AUDIENCE: str
    JWKS_CACHE_TTL_SECONDS: int = 300

    # ----------------------------
    # Build computed database URL
    # ----------------------------
    @computed_field
    @property
    def postgres_url(self) -> str:
        """Postgres URL built from individual components."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ----------------------------
    # Settings config
    # ----------------------------
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
