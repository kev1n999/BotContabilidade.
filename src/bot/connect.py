import os 
import discord 
from dotenv import load_dotenv
from discord.ext import commands
from constants.constants import BOT_PREFIX

load_dotenv()

client = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.all())

def load_commands():
    for folders in os.listdir("cogs"):
        for files in os.listdir(f"cogs/{folders}"):
            if files.endswith(".py") and not "__init__" in files:
                client.load_extension(f"cogs.{folders}.{files[:-3]}")
                
def setup():
    load_commands()
    client.run(os.getenv("BOT_TOKEN"))