import asyncio
import copy
import datetime
import random

import discord
from discord import app_commands
from discord.ext import commands

from helpers.character import Character
from helpers.puzzle import ANAGRAMS, ANAGRAMS_DATA, MIND_MELD, jumble

from .character_manage import character_db

COLOR = 0x00FF00


class MindMeldButton(discord.ui.Button["MindMeld"]):
    """A button that represents a cell in the Mind Meld game."""

    def __init__(
        self, x: int, y: int, label: str, disabled: bool, character: Character
    ) -> None:
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label=label if disabled else "\u200b",
            disabled=disabled,
            row=y,
        )
        self.x = x
        self.y = y
        self.character = character
        if self.view is not None:
            self.winning_words = self.view.get_winning_words()

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None
        view: MindMeld = self.view
        selected_btn_value = view.board[self.y][self.x]

        result = view.check_btn_values(selected_btn_value)
        if result == "next":
            self.style = discord.ButtonStyle.success
            self.label = selected_btn_value
            self.disabled = True
            content = (
                f"Correct! Keep going!\nFind `{' '.join(view.winning_words)}`"
            )

        elif result == "next_level":
            for child in view.children:
                child.style = discord.ButtonStyle.secondary
                child.label = "\u200b"
                child.disabled = False
            content = f"Correct! You have reached level `{view.game_level}`!\nFind `{' '.join(view.winning_words)}`"

        elif result == "win":
            self.character.coins += 5000
            character_db.cache_database()
            content = "You win!\nAs a reward you get `5000` coins!"
            self.style = discord.ButtonStyle.success
            for child in view.children:
                child.disabled = True

            view.stop()
        else:
            if view.game_level > 1:
                coins = 100 * view.game_level - 1
                self.character.coins += coins
                character_db.cache_database()
                content = f"Incorrect! Try again!\nYou completed `{view.game_level - 1}` levels!\nAs a reward you get `{coins}` coins!"
            else:
                content = "Incorrect! Try again!"
            self.style = discord.ButtonStyle.danger
            self.label = selected_btn_value
            for child in view.children:
                child.disabled = True

        embed = discord.Embed(
            title="Mind Meld!", description=content, color=COLOR
        )

        await interaction.response.edit_message(view=view, embed=embed)


class MindMeld(discord.ui.View):
    """The main view for the Mind Meld game."""

    children: list[MindMeldButton]
    words: list[str]

    def __init__(
        self,
        level: int,
        disabled: bool,
        words: list[str],
        winning_words: list[str],
        character: Character,
    ) -> None:
        super().__init__()
        self.level = level
        self.disabled = disabled
        self.words = words
        self.winning_words = winning_words
        self.character = character

        temp = copy.deepcopy(self.words)
        self.board = [
            [temp.pop(0) for _ in range(level)] for _ in range(level)
        ]

        self.game_level = 1

        for i in range(level):
            for j in range(level):
                self.add_item(
                    MindMeldButton(
                        i, j, self.board[j][i], self.disabled, self.character
                    )
                )

    def check_btn_values(self, selected_btn_value: str) -> str:
        if selected_btn_value == self.winning_words[0]:
            self.winning_words.pop(0)

            if self.winning_words == []:
                self.game_level += 1

                temp = copy.deepcopy(self.words)
                for _ in range(self.game_level):
                    random_word = random.choice(temp)
                    self.winning_words.append(random_word)
                    temp.remove(random_word)

                if self.game_level == len(self.words):
                    return "win"

                return "next_level"

            return "next"

        return "stop"

    def get_winning_words(self) -> list[str] | None:
        return self.winning_words


class Puzzle(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="jumble_jigger",
        description="Need for some coins? Come play this minigame",
    )
    async def jumble_jigger(self, interaction: discord.Interaction) -> None:
        character = character_db.get_character_info(interaction.user.id)

        if character == -1:
            await interaction.response.send_message(
                "You do not have a character created. Use `/create` to create one.",
                ephemeral=True,
            )
            return

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
            coins = random.randint(100, 200)
            character.coins += coins
            character_db.cache_database()

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
        character = character_db.get_character_info(interaction.user.id)

        if character == -1:
            await interaction.response.send_message(
                "You do not have a character created. Use `/create` to create one.",
                ephemeral=True,
            )
            return

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
                coins = random.randint(10, 50)
                character.coins += coins
                character_db.cache_database()

                if correct_words == []:
                    break

                embed = discord.Embed(
                    title="Correct!",
                    description=f"You guessed `{correct_guess}` words correctly!\nYou have `{len(correct_words)}` words left to guess.\nAs a reward you get `{coins}` coins!",
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

        if correct_words == []:
            character.coins += 500
            character_db.cache_database()
            embed = discord.Embed(
                title="Congratulations!",
                description="You have guessed all the words correctly!\nAs a reward you get extra `500` coins!",
                color=COLOR,
            )
            await interaction.followup.send(embed=embed)
            return

        embed = discord.Embed(
            title="Time's up!",
            description=f"You guessed `{correct_guess}` words correctly!\nRemaining words: `{', '.join(correct_words)}`\nBetter luck next time!",
            color=COLOR,
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="mind_meld",
        description="Connect your mind and match your memories in this ultimate brain battle!",
    )
    @app_commands.describe(
        level="Select a level", start_time="Select a start time"
    )
    @app_commands.choices(
        level=[
            app_commands.Choice(name="1", value=3),
            app_commands.Choice(name="2", value=4),
            app_commands.Choice(name="3", value=5),
        ]
    )
    @app_commands.choices(
        start_time=[
            app_commands.Choice(name="30 seconds", value=30),
            app_commands.Choice(name="45 seconds", value=45),
            app_commands.Choice(name="60 seconds", value=60),
        ]
    )
    async def mind_meld(
        self, interaction: discord.Interaction, level: int, start_time: int
    ) -> None:
        character = character_db.get_character_info(interaction.user.id)

        if character == -1:
            await interaction.response.send_message(
                "You do not have a character created. Use `/create` to create one.",
                ephemeral=True,
            )
            return

        temp = copy.deepcopy(MIND_MELD)
        words = [
            temp.pop(random.randint(0, len(temp) - 1)) for _ in range(level**2)
        ]
        winning_words = [random.choice(words)]

        view = MindMeld(
            level=level,
            disabled=True,
            words=words,
            winning_words=winning_words,
            character=character,
        )
        embed = discord.Embed(
            title="Mind Meld!",
            description=f"Find `{' '.join(winning_words)}`, Hurry up! You have `{start_time}` seconds remember the positions!",
            color=COLOR,
        )
        await interaction.response.send_message(
            view=view, delete_after=start_time, embed=embed
        )

        await asyncio.sleep(start_time)
        view = MindMeld(
            level=level,
            disabled=False,
            words=words,
            winning_words=winning_words,
            character=character,
        )

        embed = discord.Embed(
            title="Mind Meld!",
            description=f"Game started! Click the buttons to match the words!\n You need find `{' '.join(winning_words)}`",
            color=COLOR,
        )
        await interaction.followup.send(view=view, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Puzzle(bot))
