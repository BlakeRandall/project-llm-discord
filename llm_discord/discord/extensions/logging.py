import logging
from discord import User, Message, Member, Guild
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

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        logger.info(f"Guild Joined {guild}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        logger.info(f"Guild Left {guild}")

    @commands.Cog.listener()
    async def on_guild_update(self, before: Guild, after: Guild):
        logger.info(f"Guild (updated) {before} -> {after}")

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        logger.info(f"Member Joined {member}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        logger.info(f"Member Left {member}")

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        logger.info(f"Member (updated) {before} -> {after}")

    @commands.Cog.listener()
    async def on_user_update(self, before: User, after: User):
        logger.info(f"User (updated) {before} -> {after}")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        logger.info(f"Message {message}")

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        logger.info(f"Message (updated) {before} -> {after}")

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        logger.info(f"Message (delete) {message}")

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: list[Message]):
        for message in messages:
            logger.info(f"Message (delete) {message}")
