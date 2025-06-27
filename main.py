import os
import dotenv
import asyncio
import discord
from discord.ext import commands
import logging
from apps import player_rank

dotenv.load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

handler = logging.FileHandler(filename="discord.log", mode="w")

intents = discord.Intents.all()


bot = commands.Bot(command_prefix="*", intents=intents)


player_rank.load_players()



def rank_embed(riot_id, rank):
    embed = discord.Embed(title=riot_id, colour=discord.Color.blue())
    file = None
    match rank.tier:
        case "IRON":
            file = discord.File("img/ranks/iron.png", filename="iron.png")
        case "BRONZE":
            file = discord.File("img/ranks/bronze.png", filename="bronze.png")
        case "SILVER":
            file = discord.File("img/ranks/silver.png", filename="silver.png")
        case "GOLD":
            file = discord.File("img/ranks/gold.png", filename="gold.png")
        case "PLATINIUM":
            file = discord.File("img/ranks/platinium.png", filename="platinium.png")
        case "EMERALD":
            file = discord.File("img/ranks/emerald.png", filename="emerald.png")
        case "DIAMOND":
            file = discord.File("img/ranks/diamond.png", filename="diamond.png")
        case "MASTER":
            file = discord.File("img/ranks/master.png", filename="master.png")
        case "GRANDMASTER":
            file = discord.File("img/ranks/grandmaster.png", filename="grandmaster.png")
        case "CHALLENGER":
            file = discord.File("img/ranks/challenger.png", filename="challenger.png")



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
async def add(ctx, riot_id):
    valid = player_rank.get_ranks(riot_id)
    if valid["ranks"] == None:
        if valid["puuid_code"] != None:
            await ctx.send(f":x: Erreur account-v1 {valid['puuid_code']}")
        else :
            await ctx.send(f":x: Erreur league-v4 {valid['ranks_code']}")
    else:
        for player in player_rank.Player.players:
            if player.riot_id == riot_id :
                await ctx.send(f"{riot_id} est déjà enrengistré/e !")
                break
        else :
            player_rank.Player.add_player(player_rank.Player(riot_id))
            player_rank.save_players()
            await ctx.send(f"{riot_id} ajouté/e !")

@bot.command()
async def remove(ctx, riot_id):
    for player in player_rank.Player.players:
        if player.riot_id == riot_id :
            player_rank.Player.players.remove(player)
            player_rank.save_players()
            await ctx.send(f"{riot_id} retiré/e !")
            break
    else :
        await ctx.send("Aucun joueur correspondant")

@bot.command()
async def saved(ctx):
    if not player_rank.Player.players:
        await ctx.send("Aucun joueur enregistré.")
        return
    saved = "**Joueurs enregistrés :**\n"
    for player in player_rank.Player.players:
        saved += f"- {player.riot_id}\n"
    await ctx.send(saved)

@bot.command()
async def clear(ctx):
    await ctx.send("⚠️ Es-tu sûr de vouloir supprimer tous les joueurs ? (y/n)")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["y", "n"]

    try:
        msg = await bot.wait_for("message", check=check, timeout=15)
    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé, opération annulée.")
        return

    if msg.content.lower() == "y":
        player_rank.Player.players.clear()
        player_rank.save_players()
        await ctx.send(":put_litter_in_its_place: Tous les joueurs ont été supprimé/es !")
    else:
        await ctx.send("Opération annulée.")

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

@bot.command()
async def vs(ctx, queue, riot_id1, riot_id2):
    ranks1 = player_rank.get_ranks(riot_id1)
    ranks2 = player_rank.get_ranks(riot_id2)

    if queue == "solo":
        if ranks1["ranks"].solo.score > ranks2["ranks"].solo.score :
            await ctx.send(f"*{riot_id1}* :\n{ranks1['ranks'].solo.__str__()}\n*{riot_id2}*:\n{ranks2['ranks'].solo.__str__()}\n:trophy: {riot_id1} solo !")
        else:
            await ctx.send(f"*{riot_id1}* :\n{ranks1['ranks'].solo.__str__()}\n*{riot_id2}*:\n{ranks2['ranks'].solo.__str__()}\n:trophy: {riot_id2} solo !")
    elif queue == "flex":
        if ranks1["ranks"].flex.score > ranks2["ranks"].flex.score :
            await ctx.send(f"*{riot_id1}* :\n{ranks1['ranks'].flex.__str__()}\n*{riot_id2}*:\n{ranks2['ranks'].flex.__str__()}\n:trophy: {riot_id1} solo !")
        else:
            await ctx.send(f"*{riot_id1}* :\n{ranks1['ranks'].flex.__str__()}\n*{riot_id2}*:\n{ranks2['ranks'].flex.__str__()}\n:trophy: {riot_id2} solo !")
    else:
        await ctx.send(":x: mode de jeu incorrect")


bot.run(discord_bot_token, log_handler=handler)