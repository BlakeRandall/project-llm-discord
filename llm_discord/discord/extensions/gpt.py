import logging
from discord import Message
from discord.enums import ChannelType
from discord.ext import commands, tasks
from langchain.messages import HumanMessage
from llm_discord.discord.cogs import BaseCog
from llm_discord.agent import AgentFacade

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Loaded (Setup)")
    await bot.add_cog(GPTCog(bot))


async def teardown(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Unloaded (Teardown)")
    await bot.remove_cog(GPTCog.__cog_name__)


class GPTCog(BaseCog):
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        logger.info(f"Message {message}")
        if message.author == self.bot.user:
            return
        if message.channel.type not in [ChannelType.text]:
            return
        async with message.channel.typing():
            agent = await AgentFacade.agent()
            response = await agent.ainvoke(
                input=dict(messages=[HumanMessage(content=message.clean_content)]),
                context=dict(
                    author=message.author, channel=message.channel, message=message
                ),
                config=dict(
                    configurable=dict(
                        thread_id=message.author.id, checkpoint_ns="discord"
                    )
                ),  # type: ignore
            )
            messages = response["messages"]
            last_message = messages[-1]
            await message.channel.send(content=last_message.content, delete_after=300)

    @commands.hybrid_command()
    async def gpt(self, ctx: commands.Context[commands.Bot], content: str):
        """Message"""
        async with ctx.typing(ephemeral=True):
            agent = await AgentFacade.agent()
            response = await agent.ainvoke(
                input=dict(
                    messages=[HumanMessage(content=content)],
                ),
                context=dict(
                    author=ctx.author, channel=ctx.channel, message=ctx.message
                ),
                config=dict(
                    configurable=dict(thread_id=ctx.author.id, checkpoint_ns="discord")
                ),  # type: ignore
            )
            messages = response["messages"]
            last_message = messages[-1]
            await ctx.send(
                content=last_message.content, ephemeral=True, delete_after=300
            )
