import logging
import contextlib
import asyncio
import inspect
import importlib
import importlib.util
from discord import AllowedMentions, CustomActivity, Intents, Status
from discord.app_commands import AppCommandContext, AppInstallationType
from discord.ext import commands
from pydantic import SecretStr

logger = logging.getLogger(__name__)


class DiscordClient(commands.Bot):
    def __init__(self, *args, token: SecretStr, **kwargs) -> None:
        kwargs.setdefault("intents", Intents.all())
        kwargs.setdefault("status", Status.do_not_disturb)
        kwargs.setdefault(
            "allowed_mentions",
            AllowedMentions(
                everyone=False, roles=False, users=False, replied_user=True
            ),
        )
        kwargs.setdefault("activity", CustomActivity(name="Clanker"))
        kwargs.setdefault("case_insensitive", True)
        super().__init__(
            command_prefix=commands.bot.when_mentioned,
            help_command=None,
            allowed_contexts=AppCommandContext(
                guild=True, dm_channel=True, private_channel=True
            ),
            allowed_installs=AppInstallationType(guild=True, user=True),
            *args,
            **kwargs,
        )
        self.__token = token

    async def setup_hook(self) -> None:
        pkg = importlib.import_module(
            importlib.util.resolve_name("..extensions", __package__)
        )
        for name, _ in inspect.getmembers(pkg, lambda member: inspect.ismodule(member)):
            logger.info(f"Extension: {name} - Loaded")
            await self.load_extension(f".{name}", package=pkg.__name__)
        for command in await self.tree.sync():
            logger.info(f"AppCommand Sync: {command}")
        await super().setup_hook()

    async def close(self, *args, **kwargs):
        pkg = importlib.import_module(
            importlib.util.resolve_name("..extensions", __package__)
        )
        for name, _ in inspect.getmembers(pkg, lambda member: inspect.ismodule(member)):
            logger.info(f"Extension: {name} - Unloaded")
            await self.unload_extension(f".{name}", package=pkg.__name__)
        await super().close(*args, **kwargs)

    async def reload(self, *args, **kwargs):
        pkg = importlib.import_module(
            importlib.util.resolve_name("..extensions", __package__)
        )
        for name, _ in inspect.getmembers(pkg, lambda member: inspect.ismodule(member)):
            logger.info(f"Extension: {name} - Reloaded")
            await self.reload_extension(f".{name}", package=pkg.__name__)
        for command in await self.tree.sync():
            logger.info(f"AppCommand Sync: {command}")

    @property
    def token(self) -> SecretStr:
        return self.__token

    async def __custom_run(self):
        async with self:
            await self.start(token=self.token.get_secret_value())

    @contextlib.asynccontextmanager
    async def custom_run(self):
        task = asyncio.create_task(self.__custom_run())
        try:
            yield
        finally:
            task.cancel()
