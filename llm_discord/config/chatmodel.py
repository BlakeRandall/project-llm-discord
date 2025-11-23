import logging
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_core.language_models import BaseChatModel
from langchain.chat_models import init_chat_model

logger = logging.getLogger(__name__)


class ChatModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="chat_model_",
        env_nested_max_split=1,
        env_nested_delimiter="_",
        env_parse_enums=True,
        case_sensitive=False,
        extra="ignore",
    )

    model: str = Field(
        default="openai/gpt-oss-120b", description="The GenAI model to use", frozen=True
    )

    model_provider: str = Field(
        default="groq", description="The provider of the GenAI model", frozen=True
    )

    temperature: float = Field(
        default=0.0, description="Temperature setting for the GenAI model", frozen=True
    )

    max_tokens: int | None = Field(
        default=2**16,
        description="Maximum tokens for the GenAI model response",
        frozen=True,
    )

    api_key: SecretStr | None = Field(
        default=None, description="API key for accessing the GenAI model", frozen=True
    )

    __chat_model: BaseChatModel | None = PrivateAttr(default=None, init=False)

    @property
    def chat_model(self) -> BaseChatModel:
        if self.__chat_model is None:
            self.__chat_model = init_chat_model(
                model=self.model,
                model_provider=self.model_provider,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.api_key,
            )
        return self.__chat_model
