"""Settings management using pydantic-settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global settings for Hospital Vulnerability Scanner MCP Server."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="HOSPITAL_VULN_MCP_",
        case_sensitive=False,
        extra="ignore",
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )

    # Scanner settings
    scan_timeout: int = Field(
        default=300,
        description="Scan timeout in seconds",
    )
    max_concurrent_scans: int = Field(
        default=10,
        description="Maximum concurrent scans",
    )


settings = Settings()
