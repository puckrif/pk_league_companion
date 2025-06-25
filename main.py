import os
import json
import requests
import dotenv
import discord
from discord.ext import commands

dotenv.load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="*", intents=intents)