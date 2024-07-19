import discord
from discord import app_commands
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="test", description="Test command")
    async def test(
        self, interaction: discord.Interaction, message: str
    ) -> None:
        await interaction.response.send_message(f"Test: {message}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Test(bot))
