import logging
from datetime import datetime, timedelta, timezone
from discord.utils import sleep_until
from discord.ext import commands
from llm_discord.discord.cogs import BaseCog

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Loaded (Setup)")
    await bot.add_cog(PingPongCog(bot))


async def teardown(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Unloaded (Teardown)")
    await bot.remove_cog(PingPongCog.__cog_name__)


class PingPongCog(BaseCog):
    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context[commands.Bot]):
        """Pong"""
        now = datetime.now().astimezone(timezone.utc)
        async with ctx.typing(ephemeral=True):
            await sleep_until(now + timedelta(seconds=1))
            await ctx.send(content="pong", ephemeral=True)
