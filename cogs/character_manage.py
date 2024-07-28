import os
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from helpers.character import Character
from helpers.character_database import CharacterDatabase
from helpers.generator import ItemGenerator

# Get the data folder path
repo_path: Path = Path(__file__).parent.parent
data_fp: str = os.path.join(repo_path, "data")

# Initialize Database
character_db: CharacterDatabase = CharacterDatabase(data_path=data_fp)
item_generator: ItemGenerator = ItemGenerator(data_fp)


class Dropdown(discord.ui.Select):
    def __init__(
        self,
        placeholder: str,
        options: list[discord.SelectOption],
        custom_id: str,
    ) -> None:
        """Dropdown selection for character attributes."""
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=options,
            custom_id=custom_id,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Handle dropdown selection."""
        await interaction.response.defer()


class DropdownView(discord.ui.View):
    def __init__(self) -> None:
        """View containing dropdowns for sex, race, and class selection."""
        super().__init__()
        sex_options: list[discord.SelectOption] = [
            discord.SelectOption(
                label="Male", description="Start your life as a male."
            ),
            discord.SelectOption(
                label="Female", description="Start your life as a female."
            ),
            discord.SelectOption(
                label="Other", description="Start your life as another gender."
            ),
        ]
        race_options: list[discord.SelectOption] = [
            discord.SelectOption(
                label="Human",
                description="Adaptable and ambitious, thriving in diverse cultures.",
            ),
            discord.SelectOption(
                label="Tiefling",
                description="Marked by infernal heritage, with innate magic and resilience.",
            ),
            discord.SelectOption(
                label="Dwarf",
                description="Steadfast and skilled, valuing honor and loyalty.",
            ),
            discord.SelectOption(
                label="Elf",
                description="Graceful and long-lived, with keen senses and a deep connection to nature.",
            ),
            discord.SelectOption(
                label="Halfling",
                description="Small and cheerful, valuing comfort and luck, and adept at overcoming challenges.",
            ),
            discord.SelectOption(
                label="Gnome",
                description="Inventive and curious, living in hidden burrows and loving adventure.",
            ),
            discord.SelectOption(
                label="Half-Orc",
                description="Strong and resilient, combining orcish ferocity with human adaptability.",
            ),
            discord.SelectOption(
                label="Half-Elf",
                description="Versatile and charismatic, blending human ambition with elven grace.",
            ),
        ]
        class_options: list[discord.SelectOption] = [
            discord.SelectOption(
                label="Warrior",
                description="A Warrior is strong and resilient, skilled in melee combat and battlefield tactics.",
            ),
            discord.SelectOption(
                label="Mage",
                description="A Mage wields powerful magic, specializing in spells and arcane knowledge.",
            ),
            discord.SelectOption(
                label="Rogue",
                description="A Rogue is cunning and stealthy, excelling in deception and surprise attacks.",
            ),
        ]

        self.add_item(
            Dropdown(
                placeholder="Select sex", options=sex_options, custom_id="sex"
            )
        )
        self.add_item(
            Dropdown(
                placeholder="Select race",
                options=race_options,
                custom_id="race",
            )
        )
        self.add_item(
            Dropdown(
                placeholder="Select class",
                options=class_options,
                custom_id="class",
            )
        )
        self.add_item(SubmitButton())


class SubmitButton(discord.ui.Button):
    def __init__(self) -> None:
        """Submit button to finalize character creation."""
        super().__init__(
            label="Submit", style=discord.ButtonStyle.green, custom_id="submit"
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Handle submit button click."""
        sex: str | None = None
        race: str | None = None
        clss: str | None = None

        for child in self.view.children:  # type: ignore
            if isinstance(child, Dropdown):
                if child.custom_id == "sex":
                    sex = child.values[0] if child.values else None
                elif child.custom_id == "race":
                    race = child.values[0] if child.values else None
                elif child.custom_id == "class":
                    clss = child.values[0] if child.values else None

        if sex and race and clss:
            user_id: int = interaction.user.id

            char_info = character_db.get_character_info(user_id)
            if char_info != -1:
                await interaction.response.send_message(
                    "You already have a character created.", ephemeral=True
                )
            else:
                new_character: Character = Character()
                new_character.name = interaction.user.name
                new_character.sex = sex
                new_character.class_ = clss
                new_character.race = race

                res: int = character_db.add_character(user_id, new_character)

                if res < 0:
                    await interaction.response.send_message(
                        "You already have a character!",
                        ephemeral=True,
                        delete_after=10,
                    )
                else:
                    await interaction.response.send_message(
                        "Congratulations! You have created a character!",
                        ephemeral=True,
                        delete_after=10,
                    )
        else:
            await interaction.response.send_message(
                "Please select all options before submitting.", ephemeral=True
            )


class CharacterHandle(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Cog for handling character-related commands."""
        self.bot = bot

    @app_commands.command(
        name="create",
        description="Welcome to the world, first you need to create your character. This is the command to do so.",
    )
    async def create(self, interaction: discord.Interaction) -> None:
        """Slash command to create a character."""
        user_id: int = interaction.user.id

        char_info = character_db.get_character_info(user_id)
        if char_info != -1:
            await interaction.response.send_message(
                "You already have a character created.", ephemeral=True
            )
        else:
            view: DropdownView = DropdownView()
            embed: discord.Embed = discord.Embed(
                title="Character Selection",
                description="To begin creating your character, fill in the following dropdowns. Choose wisely!\n**This message will be deleted in 2 minutes.**",
                color=0x00FF00,
            )
            await interaction.response.send_message(
                embed=embed, view=view, delete_after=120
            )

    @app_commands.command(name="view", description="View your character.")
    async def view(self, interaction: discord.Interaction) -> None:
        """Slash command to view your character."""
        user_id: int = interaction.user.id

        character = character_db.get_character_info(user_id)

        if character != -1:
            sex, race, class_ = (
                character.sex,
                character.race,
                character.class_,
            )
            embed: discord.Embed = discord.Embed(
                title="Your Character",
                description=f"Sex: {sex}\nRace: {race}\nClass: {class_}",
                color=0x00FF00,
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "You do not have a character created.", ephemeral=True
            )

    @app_commands.command(name="balance", description="Check your balance.")
    async def balance(self, interaction: discord.Interaction) -> None:
        """Slash command to check your balance."""
        user_id: int = interaction.user.id
        character = character_db.get_character_info(user_id)

        if character == -1:
            await interaction.response.send_message(
                "You do not have a character created. Use `/create` to create one.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Your balance is `{character.coins}` coins."
            )

    @app_commands.command(
        name="checkin", description="Get everything your character has gained"
    )
    async def checkin(self, interaction: discord.Interaction) -> None:
        """Slash command to check in your character."""
        user_id: int = interaction.user.id
        check: int = character_db.character_checkin(user_id)

        if check < 0:
            await interaction.response.send_message(
                "You do not have a character created.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You have checked in your character, use /view to see changes"
            )

    @app_commands.command(
        name="gacha", description="Roll the gacha to get a random item"
    )
    async def gacha(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        character = character_db.get_character_info(user_id)

        if character == -1:
            await interaction.response.send_message(
                "You do not have a character created. Use `/create` to create one.",
                ephemeral=True,
            )
            return

        if character.coins < 500:
            await interaction.response.send_message(
                "You do not have enough coins to roll the gacha. You need at least `500` coins.",
                ephemeral=True,
            )
            return

        generated_item = item_generator.get_item()
        character.inventory.append(generated_item)
        character.coins -= 500
        character_db.cache_database()

        await interaction.response.send_message(
            f"You have rolled the gacha and received a `{generated_item.name}`."
        )


async def setup(bot: commands.Bot) -> None:
    """Setup function to add the CharacterHandle cog to the bot."""
    await bot.add_cog(CharacterHandle(bot))
