import logging
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from llm_discord.model.pydantic import BaseSettingsSingleton
from llm_discord.discord.client import DiscordClient

logger = logging.getLogger(__name__)


class DiscordConfig(BaseSettingsSingleton):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="discord_",
        env_nested_max_split=1,
        env_nested_delimiter="_",
        env_parse_enums=True,
        case_sensitive=False,
        extra="ignore",
    )

    bot_token: SecretStr = Field(frozen=True)

    __client: DiscordClient | None = PrivateAttr(default=None)

    @property
    def client(self) -> DiscordClient:
        if self.__client is None:
            self.__client = DiscordClient(token=self.bot_token)
        return self.__client
