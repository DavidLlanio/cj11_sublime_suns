from discord.ext import commands
from discord.ext.commands import Context, command


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @command(name="sync", aliases=["Sync"])
    async def sync(self, ctx: Context) -> None:
        """Globally syncs slash commands"""

        # Replace the hardcoded user IDs with your own to get Admin access
        if (
            ctx.author.id == 293926911875219456
            or ctx.author.id == 1071489894704226375
            or ctx.author.id == 1115694795705290862
            or ctx.author.id == 1190937272279912518
            or ctx.author.id == 375393568811909130
        ):
            await self.bot.tree.sync()
            await ctx.send("Tree synced")
        else:
            await ctx.send("You are not authorized to use this command")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
