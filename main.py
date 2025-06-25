import os
import dotenv
import discord
from discord.ext import commands
import logging
from apps import ranks_fetcher

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
    ranks = ranks_fetcher.get_ranks(riot_id)
    if ranks["ranks"] == None:
        if ranks["puuid_code"] != None:
            await ctx.send(f":x: Erreur account-v1 {ranks['puuid_code']}")
        else :
            await ctx.send(f":x: Erreur league-v4 {ranks['ranks_code']}")
    else :
        if ranks['ranks']['solo']['tier'] != None :
            solo = f"En SoloQ/DuoQ {riot_id} est {ranks['ranks']['solo']['tier']} {ranks['ranks']['solo']['rank']} avec {ranks['ranks']['solo']['leaguePoints']} LP"
            await ctx.send(solo)
        if ranks['ranks']['flex']['tier'] != None :
            flex = f"En Flex {riot_id} est {ranks['ranks']['flex']['tier']} {ranks['ranks']['flex']['rank']} avec {ranks['ranks']['flex']['leaguePoints']} LP"
            await ctx.send(flex)
        if ranks['ranks']['solo']['tier'] == None and ranks['ranks']['flex']['tier'] == None:
            await ctx.send(":warning: Pas de rangs disponible")




bot.run(discord_bot_token, log_handler=handler)