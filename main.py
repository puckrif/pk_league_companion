import os
import dotenv
import discord
from discord.ext import commands
import logging
from apps import player_rank

dotenv.load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

handler = logging.FileHandler(filename="discord.log", mode="w")

intents = discord.Intents.all()


bot = commands.Bot(command_prefix="*", intents=intents)



@bot.event
async def on_ready():
    print(f"{bot.user} is ready !")


@bot.command()
async def puck(ctx):
    file = discord.File("img/puck.gif", filename="puck.gif")
    embed = discord.Embed(colour=discord.Colour.blue(), title="Le GOAT")
    embed.set_image(url="attachment://puck.gif")
    await ctx.send(embed=embed, file=file)

@bot.command()
async def rank(ctx, riot_id):
    ranks = player_rank.get_ranks(riot_id)
    if ranks["ranks"] == None:
        if ranks["puuid_code"] != None:
            await ctx.send(f":x: Erreur account-v1 {ranks['puuid_code']}")
        else :
            await ctx.send(f":x: Erreur league-v4 {ranks['ranks_code']}")
    else :
        await ctx.send(ranks["ranks"].__str__())



bot.run(discord_bot_token, log_handler=handler)