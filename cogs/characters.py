import sqlite3

import discord
from discord import app_commands
from discord.ext import commands

conn = sqlite3.connect("characters.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS characters
             (user_id INTEGER PRIMARY KEY, sex TEXT, race TEXT, class TEXT)""")
conn.commit()


class Dropdown(discord.ui.Select):
    def __init__(self, placeholder, options, custom_id):
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=options,
            custom_id=custom_id,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()


class SubmitButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Submit", style=discord.ButtonStyle.green, custom_id="submit"
        )

    async def callback(self, interaction: discord.Interaction):
        sex = None
        race = None
        class_ = None

        for child in self.view.children:
            if isinstance(child, Dropdown):
                if child.custom_id == "sex":
                    sex = child.values[0] if child.values else None
                elif child.custom_id == "race":
                    race = child.values[0] if child.values else None
                elif child.custom_id == "class":
                    class_ = child.values[0] if child.values else None

        if sex and race and class_:
            user_id = interaction.user.id

            c.execute("SELECT * FROM characters WHERE user_id=?", (user_id,))
            if c.fetchone():
                await interaction.response.send_message(
                    "You already have a character created.", ephemeral=True
                )
            else:
                c.execute(
                    "INSERT INTO characters (user_id, sex, race, class) VALUES (?, ?, ?, ?)",
                    (user_id, sex, race, class_),
                )
                conn.commit()
                await interaction.response.send_message(
                    "Congratulations! You have created a character!",
                    ephemeral=True,
                    delete_after=10,
                )
        else:
            await interaction.response.send_message(
                "Please select all options before submitting.", ephemeral=True
            )


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        sex_options = [
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
        race_options = [
            discord.SelectOption(
                label="Human", description="Adaptable and ambitious, thriving in diverse cultures."
            ),
            discord.SelectOption(
                label="Tiefling", description="Marked by infernal heritage, with innate magic and resilience."
            ),
            discord.SelectOption(
                label="Dwarf", description="Steadfast and skilled, valuing honor and loyalty."
            ),
            discord.SelectOption(
                label="Elf", description="Graceful and long-lived, with keen senses and a deep connection to nature."
            ),
            discord.SelectOption(
                label="Halfling", description="Small and cheerful, valuing comfort and luck, and adept at overcoming challenges."
            ),
            discord.SelectOption(
                label="Gnome", description="Inventive and curious, living in hidden burrows and loving adventure."
            ),
            discord.SelectOption(
                label="Half-Orc", description="Strong and resilient, combining orcish ferocity with human adaptability."
            ),
            discord.SelectOption(
                label="Half-Elf", description="Versatile and charismatic, blending human ambition with elven grace."
            ),
        ]
        class_options = [
            discord.SelectOption(
                label="Warrior", description="A Warrior is strong and resilient, skilled in melee combat and battlefield tactics."
            ),
            discord.SelectOption(
                label="Mage", description="A Mage wields powerful magic, specializing in spells and arcane knowledge."
            ),
            discord.SelectOption(
                label="Rogue", description="A Rogue is cunning and stealthy, excelling in deception and surprise attacks."
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


class Characters(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="create",
        description="Welcome to the world, first you need to create your character. This is the command to do so.",
    )
    async def create(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        c.execute("SELECT * FROM characters WHERE user_id=?", (user_id,))
        if c.fetchone():
            await interaction.response.send_message(
                "You already have a character created.", ephemeral=True
            )
        else:
            view = DropdownView()
            embed = discord.Embed(
                title="Character Selection",
                description="To begin creating your character, fill in the following dropdowns. Choose wisely!\n**This message will be deleted in 2 minutes.**",
                color=0x00FF00,
            )
            await interaction.response.send_message(embed=embed, view=view, delete_after=120)

    @app_commands.command(name="view", description="View your character.")
    async def view(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        c.execute(
            "SELECT sex, race, class FROM characters WHERE user_id=?",
            (user_id,),
        )
        character = c.fetchone()

        if character:
            sex, race, class_ = character
            embed = discord.Embed(
                title="Your Character",
                description=f"Sex: {sex}\nRace: {race}\nClass: {class_}",
                color=0x00FF00,
            )
            await interaction.response.send_message(
                embed=embed, ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You do not have a character created.", ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Characters(bot))
