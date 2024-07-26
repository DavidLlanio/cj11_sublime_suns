import json
import random

import discord
from discord import app_commands
from discord.ext import commands

from helpers.jumble_puzzle import jumble


class Puzzle(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # TODO: Change the command name and description
    @app_commands.command(
        name="jumble_words", description="Jumble Words Puzzle"
    )
    async def jumble_words(self, interaction: discord.Interaction) -> None:
        word, jumbled_word = jumble()
        await interaction.response.send_message(
            f"Unscramble the word: `{jumbled_word}`\nYou have 60 seconds to respond."
        )

        def check(message: discord.Message) -> bool:
            return message.author == interaction.user

        try:
            message = await self.bot.wait_for(
                "message", check=check, timeout=60
            )
        except TimeoutError:
            await interaction.followup.send("Ding ding! Time's up!")
            return

        if message.content.lower() == word:
            coins = random.randint(1, 100)
            try:
                with open("./data/coins.json", "r+") as f:
                    data = json.load(f)
                    data[str(interaction.user.id)] = (
                        data.get(str(interaction.user.id), 0) + coins
                    )
                    f.seek(0)
                    json.dump(data, f, indent=4)
            except Exception:
                await interaction.followup.send(
                    "An error occurred while giving you coins. Please send a screenshot of this message to the developer to get your coins."
                )

            await interaction.followup.send(
                f"Correct!, As a reward you get `{coins}` coins!"
            )
        else:
            await interaction.followup.send("Incorrect! Try again.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Puzzle(bot))
