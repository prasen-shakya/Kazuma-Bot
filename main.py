import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('token')
bot_prefix = "#"

cogs_folder = "./cogs"

kazuma_bot = commands.Bot(command_prefix=bot_prefix)


@kazuma_bot.event
async def on_ready():
    await kazuma_bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{bot_prefix}meme help"))

for file in os.listdir(cogs_folder):
    if file.endswith(".py"):
        try:
            kazuma_bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded: {file}")
        except Exception as e:
            print(f"Could not load: {file}")
            print(e)


kazuma_bot.run(bot_token)
