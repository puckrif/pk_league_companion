import os
import datetime
import dotenv
import requests
import json

from apps import puuid_fetcher
# import puuid_fetcher

dotenv.load_dotenv()
riot_api_key = os.getenv("RIOT_API_KEY")

link = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-puuid/"


class Player():
    def __init__(self, riot_id):
        self.riot_id = riot_id
        self.player_ranks = []

    def add_ranks(self, player_rank):
        self.player_ranks = [player_rank] + self.player_ranks

    def dico(self):
        player_ranks_dico = []
        for player_rank in self.player_ranks:
            player_ranks_dico.append(player_rank.dico())
        return {
            "riot_id": self.riot_id,
            "player_ranks": player_ranks_dico
        }
    
    players = []

    @classmethod
    def add_player(cls, player):
        cls.players.append(player)
    
    @classmethod
    def cls_dico(cls):
        players_dico = []
        for player in cls.players:
            players_dico.append(player.dico())
        return players_dico


class PlayerRanks():
    def __init__(self, date, solo=None, flex=None):
        self.date = date
        self.solo = solo
        self.flex = flex

    def dico(self):
        return {
            "date": self.date.strftime("%d-%m-%Y %H:%M"),
            "solo": self.solo.dico() if self.solo != None else None,
            "flex": self.flex.dico() if self.flex != None else None
        }

    def __str__(self):
        result =  f"Le *{self.date.__str__()}*"
        if self.solo != None :
            result += "\n" + self.solo.__str__()
        if self.flex != None :
            result += "\n" + self.flex.__str__()
        if self.solo == None and self.flex == None :
            result += "\nAucun rang disponible"
        return result
    


class Rank():
    def __init__(self, queue_type, tier, lp, rank=None):
        self.queue_type = queue_type
        self.tier = tier
        self.rank = rank
        self.lp = lp
        self.score = get_score(self)

    def dico(self):
        return {
            "queue": self.queue_type,
            "tier": self.tier,
            "rank": self.rank,
            "lp": self.lp,
            "score": self.score
        }

    def __str__(self):
        if self.rank != None :
            return f"En {self.queue_type}, {self.tier} {self.rank} avec {self.lp} LP "
        else :
            return f"En {self.queue_type}, {self.tier} avec {self.lp} LP "



def save_players():
    with open("players.json", "w") as file :
        json.dump(Player.cls_dico(), file)

def load_players():
    with open("players.json", "r") as file :
        try :
            players_dico = json.load(file)
        except :
            return
        for player_dico in players_dico :
            player = Player(player_dico["riot_id"])
            for player_rank in player_dico["player_ranks"]:
                date = datetime.datetime.strptime(player_rank["date"], "%d-%m-%Y %H:%M")
                solo = None
                flex = None
                if player_rank["solo"] != None:
                    if player_rank["solo"]["rank"] != None :
                        solo = Rank(player_rank["solo"]["queue"], player_rank["solo"]["tier"], int(player_rank["solo"]["lp"]), rank=player_rank["solo"]["rank"])
                    else :
                        solo = Rank(player_rank["solo"]["queue"], player_rank["solo"]["tier"], int(player_rank["solo"]["lp"]))
                if player_rank["flex"] != None:
                    if player_rank["flex"]["rank"] != None :
                        flex = Rank(player_rank["flex"]["queue"], player_rank["flex"]["tier"], int(player_rank["flex"]["lp"]), rank=player_rank["flex"]["rank"])
                    else :
                        flex = Rank(player_rank["flex"]["queue"], player_rank["flex"]["tier"], int(player_rank["flex"]["lp"]))
                ranks = PlayerRanks(date, solo, flex)
                player.add_ranks(ranks)
            Player.add_player(player)



def get_ranks_raw(riot_id):
    puuid = puuid_fetcher.get_puuid(riot_id)
    if puuid["puuid_code"] == 200:
        ranks_raw = requests.get(f"{link}{puuid['puuid']}?api_key={riot_api_key}")
        if ranks_raw.status_code == 200:
            ranks = ranks_raw.json()
        else :
            ranks = None
        return {"ranks": ranks, "puuid_code": puuid["puuid_code"], "ranks_code": ranks_raw.status_code}
    else :
        return {"ranks": None, "puuid_code": puuid["puuid_code"], "ranks_code": None}
    

def get_score(rank):
    score = 0

    match rank.rank:
        case "I":
            score += 300
        case "II":
            score += 200
        case "III":
            score += 100
        case "IV":
            score += 0
        case None :
            score += 0

    match rank.tier:
        case "IRON":
            score += 0
        case "BRONZE":
            score += 1000
        case "SILVER":
            score += 2000
        case "GOLD":
            score += 3000
        case "PLATINIUM":
            score += 4000
        case "EMERALD":
            score += 5000
        case "DIAMOND":
            score += 6000
        case "MASTER":
            score += 7000
        case "GRANDMASTER":
            score += 10000
        case "CHALLENGER":
            score += 20000

    score += rank.lp
    return score


def get_ranks(riot_id):
    response = get_ranks_raw(riot_id)
    if response["ranks"] != None:
        ranks_raw = response["ranks"]
        solo = None
        flex = None
        for queue in ranks_raw:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                try :
                    rank = queue["rank"]
                except :
                    rank = None
                solo = Rank(queue_type="Solo", tier=queue["tier"], lp=int(queue["leaguePoints"]), rank=rank)
            if queue["queueType"] == "RANKED_FLEX_SR":
                try :
                    rank = queue["rank"]
                except :
                    rank = None
                flex = Rank(queue_type="Flex", tier=queue["tier"], lp=int(queue["leaguePoints"]), rank=rank)
            ranks = PlayerRanks(date =datetime.datetime.now(), solo=solo, flex=flex)
        for player in Player.players:
            if player.riot_id == riot_id :
                player.add_ranks(ranks)
                save_players()
    else :
        ranks = None
    return {"ranks": ranks, "puuid_code": response["puuid_code"], "ranks_code": response["ranks_code"]}


if __name__ == "__main__":

    print(get_ranks("pkrf#728")["ranks"].__str__())