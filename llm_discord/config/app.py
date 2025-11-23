from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="app_",
        env_nested_max_split=1,
        env_nested_delimiter="_",
        env_parse_enums=True,
        case_sensitive=False,
        extra="ignore",
    )

    log_level: int | str = Field(
        default="INFO", description="Logging level for the application", frozen=True
    )

    host: str = Field(
        default="0.0.0.0", description="Host address for the application", frozen=True
    )

    port: int = Field(
        default=8080, description="Port number for the application", frozen=True
    )
