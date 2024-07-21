import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="test", description="Test command")
    async def test(
        self, interaction: discord.Interaction, message: str
    ) -> None:
        """Test command description"""
        await interaction.response.send_message(f"Test message: {message}")

    @app_commands.command(name="choice", description="Choice command")
    @app_commands.describe(number="Select a number")
    @app_commands.choices(
        number=[Choice(name="1", value=1), Choice(name="2", value=2)]
    )
    async def choice(
        self, interaction: discord.Interaction, number: int
    ) -> None:
        """Choice command description"""
        await interaction.response.send_message(
            f"Number: {number}", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Test(bot))
