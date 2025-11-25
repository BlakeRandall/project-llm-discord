import logging
import importlib.util
import inspect
from discord.app_commands import rename
from discord.ext import commands
from llm_discord.discord.cogs import BaseCog
from llm_discord.discord.checks import ownership_check

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Loaded (Setup)")
    await bot.add_cog(ExtManagerCog(bot))


async def teardown(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Unloaded (Teardown)")
    await bot.remove_cog(ExtManagerCog.__cog_name__)


class ExtManagerCog(BaseCog):
    @commands.hybrid_command()
    @ownership_check()
    @rename(ext_name="extension")
    async def reload(
        self, ctx: commands.Context[commands.Bot], ext_name: str | None = None
    ):
        """Reload Extensions"""
        async with ctx.typing(ephemeral=True):
            pkg = importlib.import_module(importlib.util.resolve_name(".", __package__))
            for name, _ in inspect.getmembers(
                pkg, lambda member: inspect.ismodule(member)
            ):
                if not (name == ext_name or ext_name is None):
                    continue
                logger.info(f"Extension: {name} - Reloaded")
                await ctx.bot.reload_extension(f".{name}", package=pkg.__name__)
            for command in await ctx.bot.tree.sync():
                logger.info(f"AppCommand Sync: {command}")
            await ctx.send(
                content="Extensions Reloaded", ephemeral=True, delete_after=300
            )
