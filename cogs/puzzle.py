import copy
import datetime
import json
import random

import discord
from discord import app_commands
from discord.ext import commands

from helpers.puzzle import ANAGRAMS, ANAGRAMS_DATA, jumble

COLOR = 0x00FF00


class Puzzle(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="jumble_jigger",
        description="Need for some coins? Come play this minigame",
    )
    async def jumble_jigger(self, interaction: discord.Interaction) -> None:
        word, jumbled_word = jumble()
        embed = discord.Embed(
            title="Jumble Jigger!",
            description=f"Unscramble the word: `{jumbled_word}`\nYou have 60 seconds to respond.",
            color=COLOR,
        )
        await interaction.response.send_message(embed=embed)

        def check(message: discord.Message) -> bool:
            return message.author == interaction.user

        try:
            message = await self.bot.wait_for(
                "message", check=check, timeout=60
            )
        except TimeoutError:
            embed = discord.Embed(
                title="Time's up!",
                description=f"The correct word was `{word}`.",
                color=COLOR,
            )
            await interaction.followup.send(embed=embed)
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
                return

            embed = discord.Embed(
                title="Correct!",
                description=f"As a reward you get `{coins}` coins!",
                color=COLOR,
            )
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Incorrect!",
                description=f"The correct word was `{word}`.",
                color=COLOR,
            )
            await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="anagram_adventure",
        description="Get ready for an anagram adventure! Guess as many words as you can!",
    )
    async def anagram_adventure(
        self, interaction: discord.Interaction
    ) -> None:
        word = random.choice(ANAGRAMS)
        correct_words = copy.deepcopy(ANAGRAMS_DATA[word])

        embed = discord.Embed(
            title="Anagram Adventure!",
            description=f"Your word is: `{word}`\nThere are {len(correct_words)} correct words.\nCreate as many words as you can using the letters in the word above. You have 2 minutes!\n\n Type `stop` to end the game.",
            color=COLOR,
        )
        await interaction.response.send_message(embed=embed)

        def check(message: discord.Message) -> bool:
            return message.author == interaction.user

        correct_guess = 0
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=120)
        while datetime.datetime.now() < end_time:
            try:
                message = await self.bot.wait_for(
                    "message", check=check, timeout=120
                )
                if message.content.lower() == "stop":
                    break
            except TimeoutError:
                break

            if message.content.lower() in correct_words:
                correct_guess += 1
                correct_words.remove(message.content.lower())
                embed = discord.Embed(
                    title="Correct!",
                    description=f"You guessed `{correct_guess}` words correctly!\nYou have `{len(correct_words)}` words left to guess.",
                    color=COLOR,
                )
                await interaction.followup.send(embed=embed)
            else:
                # replacing all characters except the first and last with *
                hint = random.choice(correct_words)
                hint = hint[0] + "*" * (len(hint) - 2) + hint[-1]

                embed = discord.Embed(
                    title="Incorrect!",
                    description=f"Here is a hint: `{hint}`\nYou have `{len(correct_words)}` words left to guess.",
                    color=COLOR,
                )
                await interaction.followup.send(embed=embed)

        embed = discord.Embed(
            title="Time's up!",
            description=f"You guessed `{correct_guess}` words correctly!\nRemaining words: `{', '.join(correct_words)}`\nBetter luck next time!",
            color=COLOR,
        )

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Puzzle(bot))
