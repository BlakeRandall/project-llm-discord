import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


class BaseGroupCog(commands.GroupCog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot = bot
        super().__init__()

    @property
    def bot(self) -> commands.Bot:
        return self.__bot


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.__bot = bot
        super().__init__()

    @property
    def bot(self) -> commands.Bot:
        return self.__bot

    async def cog_load(self):
        logger.info(
            f"Cog Group: {self.__cog_group_name__} - Cog: {self.__cog_name__} - Loaded"
        )

    async def cog_unload(self):
        logger.info(
            f"Cog Group: {self.__cog_group_name__} - Cog: {self.__cog_name__} - Unloaded"
        )
