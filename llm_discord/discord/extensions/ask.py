import logging
from discord.ext import commands
from langchain.messages import HumanMessage
from llm_discord.discord.cogs import BaseCog
from llm_discord.agent import AgentFacade

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Loaded (Setup)")
    await bot.add_cog(ASKCog(bot))


async def teardown(bot: commands.Bot):
    logger.info(f"Extension: {__name__} - Unloaded (Teardown)")
    await bot.remove_cog(ASKCog.__cog_name__)


class ASKCog(BaseCog):
    @commands.hybrid_command()
    async def ask(self, ctx: commands.Context[commands.Bot], content: str):
        """ASK AI"""
        async with ctx.typing(ephemeral=True):
            try:
                agent = await AgentFacade.agent()
                response = await agent.ainvoke(
                    input=dict(
                        messages=[HumanMessage(content=content)],
                    ),
                    context=dict(
                        author=ctx.author, channel=ctx.channel, message=ctx.message
                    ),
                    config=dict(
                        configurable=dict(
                            thread_id=ctx.author.id, checkpoint_ns="discord"
                        )
                    ),  # type: ignore
                )
                messages = response["messages"]
                last_message = messages[-1]
                await ctx.send(content=last_message.content)
            except:
                logger.exception("asking cog exception")
                await ctx.send(content="Apologies I crashed out.")
                raise
