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
    file = discord.File(f"img/ranks/{rank.tier.lower()}.png", filename=f"{rank.tier.lower()}.png")
    embed.set_thumbnail(url=f"attachment://{rank.tier.lower()}.png")
    embed.add_field(name=rank.queue_type.capitalize(), value=rank.__str__(), inline=True)
    return (embed, file)



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
    elif ranks["ranks"] == "Vide":
        await ctx.send(":no_mouth: Pas de rangs disponibles")
    else :
        if ranks["ranks"].solo != None:
            embed = rank_embed(riot_id, ranks["ranks"].solo)
            await ctx.send(embed=embed[0], file=embed[1])
        if ranks["ranks"].flex != None:
            embed = rank_embed(riot_id, ranks["ranks"].flex)
            await ctx.send(embed=embed[0], file=embed[1])

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
            await ctx.send(f":o: {riot_id} ajouté/e !")

@bot.command()
async def remove(ctx, riot_id):
    for player in player_rank.Player.players:
        if player.riot_id == riot_id :
            player_rank.Player.players.remove(player)
            player_rank.save_players()
            await ctx.send(f":wave: {riot_id} retiré/e !")
            break
    else :
        await ctx.send(":x: Aucun joueur correspondant")

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
async def history(ctx, riot_id, nb=5):
    for player in player_rank.Player.players:
        if player.riot_id == riot_id:
            if not player.player_ranks:
                await ctx.send("Aucun historique pour ce joueur.")
                return
            embed = discord.Embed(
                title=f"Historique de {riot_id}",
                colour=discord.Colour.blue()
            )
            solo_score = 0
            flex_score = 0
            for rank in player.player_ranks[:nb]:
                    new_solo_score = None
                    new_flex_score = None
                    if rank.solo != None:
                        new_solo_score = rank.solo.score
                    else :
                        new_solo_score = solo_score
                    if rank.flex != None:
                        new_flex_score = rank.flex.score
                    else :
                        new_flex_score = flex_score
                    if not (new_solo_score == solo_score and new_flex_score == flex_score):
                        embed.add_field(
                            name=rank.date.strftime("%d/%m/%Y %H:%M"),
                            value=rank.__str__(),
                            inline=False
                        )
                        solo_score = new_solo_score
                        flex_score = new_flex_score
            await ctx.send(embed=embed)
            return
    await ctx.send(":x: Joueur non trouvé.")

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