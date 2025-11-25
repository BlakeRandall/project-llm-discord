import logging
from discord import User, Member, AppInfo
from discord.ext import commands

logger = logging.getLogger(__name__)


def _ownership_check(author: User | Member, app_info: AppInfo):
    return any(
        [
            owner_check
            for owner_check in [
                author.id == app_info.owner.id,
                app_info.team
                and app_info.team.owner
                and author.id == app_info.team.owner.id,
                app_info.team
                and app_info.team.members
                and author.id in [member.id for member in app_info.team.members],
            ]
        ]
    )


def ownership_check():
    async def predicate(ctx: commands.Context[commands.Bot]):
        try:
            app_info = ctx.bot.application
            if not app_info:
                app_info = await ctx.bot.application_info()

            return _ownership_check(ctx.author, app_info)
        except:
            logger.exception("ownership check failure")
        return False

    return commands.check(predicate)
