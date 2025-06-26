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

@bot.command()
async def add_player(ctx, riot_id):
    valid = player_rank.get_ranks(riot_id)
    if valid["ranks"] == None:
        if valid["puuid_code"] != None:
            await ctx.send(f":x: Erreur account-v1 {valid['puuid_code']}")
        else :
            await ctx.send(f":x: Erreur league-v4 {valid['ranks_code']}")
    for player in player_rank.Player.players:
        if player.riot_id == riot_id :
            await ctx.send(f"{riot_id} est déjà enrengistré/e !")
            break
    else :
        player_rank.Player.add_player(player_rank.Player(riot_id))
        player_rank.save_players()
        await ctx.send(f"{riot_id} ajouté/e !")

@bot.command()
async def remove_player(ctx, riot_id):
    for player in player_rank.Player.players:
        if player.riot_id == riot_id :
            player_rank.Player.players.remove(player)
            player_rank.save_players()
            await ctx.send(f"{riot_id} retiré/e !")
            break
    else :
        await ctx.send("Aucun joueur correspondant")

@bot.command()
async def saved_players(ctx):
    if not player_rank.Player.players:
        await ctx.send("Aucun joueur enregistré.")
        return
    saved = "**Joueurs enregistrés :**\n"
    for player in player_rank.Player.players:
        saved += f"- {player.riot_id}\n"
    await ctx.send(saved)

@bot.command()
async def history(ctx, riot_id):
    for player in player_rank.Player.players:
        if player.riot_id == riot_id :
            history = "**Historique :**\n\n"
            for ranks in player.player_ranks:
                history += f"{ranks.__str__()}\n--------------\n"
            await ctx.send(history)
            break
    else :
        await ctx.send("Aucun joueur correspondant")


bot.run(discord_bot_token, log_handler=handler)