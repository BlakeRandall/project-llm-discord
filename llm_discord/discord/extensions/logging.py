import logging
from discord.ext import commands
from llm_discord.discord.cogs import BaseCog

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Loaded (Setup)")
    await bot.add_cog(LoggingCog(bot))


async def teardown(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Unloaded (Teardown)")
    await bot.remove_cog(LoggingCog.__cog_name__)


class LoggingCog(BaseCog):
    @commands.Cog.listener()
    async def on_connect(self):
        logger.info("Connected")

    @commands.Cog.listener()
    async def on_disconnect(self):
        logger.info("Disconnected")

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Ready")

    @commands.Cog.listener()
    async def on_resumed(self):
        logger.info("Resumed")

    @commands.Cog.listener()
    async def on_shard_ready(self):
        logger.info("Shard Ready")

    @commands.Cog.listener()
    async def on_shard_resumed(self):
        logger.info("Shard Resumed")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        logger.exception(f"Error on Event {event}")
