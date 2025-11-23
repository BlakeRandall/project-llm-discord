import logging
import contextlib
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from llm_discord.config.app import AppConfig
from llm_discord.config.discord import DiscordConfig
from llm_discord.logging import setup_logging
from llm_discord.mcp import mcp
from llm_discord.api import api

setup_logging()

logger = logging.getLogger(__name__)

app_config = AppConfig()
discord_config = DiscordConfig()


@contextlib.asynccontextmanager
async def lifespan(_: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        await stack.enter_async_context(discord_config.client.custom_run())
        yield


api = Starlette(
    routes=[
        Mount(path="/mcp/", app=mcp.streamable_http_app()),
        Mount(path="/api/", app=api),
    ],
    lifespan=lifespan,
)

uvicorn.run(api, host=app_config.host, port=app_config.port)
