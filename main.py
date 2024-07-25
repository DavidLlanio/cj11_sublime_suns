import os
import sqlite3

import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from dotenv import load_dotenv

load_dotenv()

if os.getenv("PURGE_DB") == "True":
    os.remove("sublime_suns.db")

CONNECTION = sqlite3.connect("sublime_suns.db")
CURSOR = CONNECTION.cursor()

bot: Bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    # loding cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

    print(f"{bot.user} has connected to Discord!")


if __name__ == "__main__":
    CURSOR.execute("""CREATE TABLE IF NOT EXISTS characters
                (user_id INTEGER PRIMARY KEY, sex TEXT, race TEXT, class TEXT)""")

    # TODO: Add more tables here if needed

    CONNECTION.commit()

    try:
        bot.run(os.getenv("TOKEN"))  # type: ignore
    except Exception as e:
        print(f"Failed to start the bot. Error: {e}")
