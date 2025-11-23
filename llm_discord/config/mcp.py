import logging
import itertools
import asyncio
import pathlib
import yaml
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain.tools import BaseTool
from langchain.messages import AIMessage, HumanMessage
from langchain_core.documents.base import Blob
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.sessions import Connection
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.prompts import load_mcp_prompt
from langchain_mcp_adapters.resources import load_mcp_resources

logger = logging.getLogger(__name__)


class MCPConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="mcp_",
        env_nested_max_split=1,
        env_nested_delimiter="_",
        env_parse_enums=True,
        case_sensitive=False,
        extra="ignore",
    )

    config: pathlib.Path = Field(default=pathlib.Path("mcp.yml"), frozen=True)

    __connections: dict[str, Connection] = PrivateAttr(default_factory=dict, init=False)

    __multi_mcp_client: MultiServerMCPClient | None = PrivateAttr(
        default=None, init=False
    )

    def model_post_init(self, context: Any) -> None:
        if self.config.exists():
            with self.config.open("r") as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    for connection_name, connection_info in config_data.items():
                        self.__connections[connection_name] = connection_info
        super().model_post_init(context)

    @property
    def connections(self) -> dict[str, Connection]:
        return self.__connections

    @property
    def multi_mcp_client(self) -> MultiServerMCPClient:
        if self.__multi_mcp_client is None:
            self.__multi_mcp_client = MultiServerMCPClient(
                connections=self.__connections
            )
        return self.__multi_mcp_client

    async def tools(self, *, server_name: str | None = None) -> list[BaseTool]:
        async def _tools(connection: Connection) -> list[BaseTool]:
            tools = []
            try:
                tools.extend(await load_mcp_tools(session=None, connection=connection))
            except:
                logger.exception("Load MCP Tools Failure")
            return tools

        return [
            tool
            for tool in itertools.chain(
                *await asyncio.gather(
                    *[
                        asyncio.create_task(_tools(connection))
                        for name, connection in self.connections.items()
                        if name == server_name or server_name is None
                    ]
                )
            )
        ]

    async def prompts(
        self,
        server_name: str,
        prompt_name: str,
        *,
        arguments: dict[str, Any] | None = None,
    ) -> list[HumanMessage | AIMessage]:
        async with self.multi_mcp_client.session(server_name) as session:
            return await load_mcp_prompt(session, prompt_name, arguments=arguments)

    async def resources(
        self, server_name: str, *, uris: str | list[str] | None = None
    ) -> list[Blob]:
        async with self.multi_mcp_client.session(server_name) as session:
            return await load_mcp_resources(session, uris=uris)
