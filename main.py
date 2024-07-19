import os

import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from dotenv import load_dotenv

load_dotenv()

bot: Bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    # loding cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

    print(f"{bot.user} has connected to Discord!")


if __name__ == "__main__":
    try:
        bot.run(os.getenv("TOKEN"))  # type: ignore
    except Exception as e:
        print(f"Failed to start the bot. Error: {e}")
