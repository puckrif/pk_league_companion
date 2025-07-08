import json
import datetime
from apps import player_rank


def save_players():
    with open("players.json", "w") as file :
        json.dump(player_rank.Player.cls_dico(), file)


def load_players():
    with open("players.json", "r") as file :
        try :
            players_dico = json.load(file)
        except :
            return
        for player_dico in players_dico :
            player = player_rank.Player(player_dico["riot_id"])
            for rank in player_dico["player_ranks"]:
                date = datetime.datetime.strptime(rank["date"], "%d-%m-%Y %H:%M:%S")
                solo = None
                flex = None
                if rank["solo"] != None:
                    if rank["solo"]["rank"] != None :
                        solo = player_rank.Rank(rank["solo"]["queue"], rank["solo"]["tier"], int(rank["solo"]["lp"]), rank=rank["solo"]["rank"], score=int(rank["solo"]["score"]))
                    else :
                        solo = player_rank.Rank(rank["solo"]["queue"], rank["solo"]["tier"], int(rank["solo"]["lp"]), score=int(rank["solo"]["score"]))
                if rank["flex"] != None:
                    if rank["flex"]["rank"] != None :
                        flex = player_rank.Rank(rank["flex"]["queue"], rank["flex"]["tier"], int(rank["flex"]["lp"]), rank=rank["flex"]["rank"], score=int(rank["flex"]["score"]))
                    else :
                        flex = player_rank.Rank(rank["flex"]["queue"], rank["flex"]["tier"], int(rank["flex"]["lp"]), score=int(rank["flex"]["score"]))
                ranks = player_rank.PlayerRanks(date, solo, flex)
                player.add_ranks(ranks)
            player_rank.Player.add_player(player)
