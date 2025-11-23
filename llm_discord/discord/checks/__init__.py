import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


def ownership_check():
    async def predicate(ctx: commands.Context[commands.Bot]):
        try:
            app_info = ctx.bot.application
            if not app_info:
                app_info = await ctx.bot.application_info()

            return any(
                [
                    owner_check
                    for owner_check in [
                        ctx.author.id == app_info.owner.id,
                        app_info.team
                        and app_info.team.owner
                        and ctx.author.id == app_info.team.owner.id,
                        app_info.team
                        and app_info.team.members
                        and ctx.author.id
                        in [member.id for member in app_info.team.members],
                    ]
                ]
            )
        except:
            logger.exception("ownership check failure")
        return False

    return commands.check(predicate)
