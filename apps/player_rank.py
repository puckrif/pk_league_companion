import os
import datetime
import dotenv
import requests

from apps import puuid_fetcher
# import puuid_fetcher

dotenv.load_dotenv()
riot_api_key = os.getenv("RIOT_API_KEY")

link = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-puuid/"


class Player():
    def __init__(self, riot_id):
        self.riot_id = riot_id
        self.player_ranks = []
    
    players = []

    @classmethod
    def add_player(cls, player):
        cls.players.append(player)


class PlayerRanks():
    def __init__(self, solo=None, flex=None):
        self.date = datetime.datetime.now()
        self.solo = solo
        self.flex = flex

    def __str__(self):
        result =  f"Le {self.date.__str__()}"
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

    def __str__(self):
        if self.rank != None :
            return f"En {self.queue_type}, {self.tier} {self.rank} avec {self.lp} LP "
        else :
            return f"En {self.queue_type}, {self.tier} avec {self.lp} LP "


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
    

def get_score(ranks):
    score = 0

    match ranks["rank"]:
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

    match ranks["tier"]:
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

    score += int(ranks["leaguePoints"])
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
                solo = Rank(queue_type="Solo", tier=queue["tier"], lp=queue["leaguePoints"], rank=rank)
            if queue["queueType"] == "RANKED_FLEX_SR":
                try :
                    rank = queue["rank"]
                except :
                    rank = None
                flex = Rank(queue_type="Flex", tier=queue["tier"], lp=queue["leaguePoints"], rank=rank)
            ranks = PlayerRanks(solo=solo, flex=flex)
    else :
        ranks = None
    return {"ranks": ranks, "puuid_code": response["puuid_code"], "ranks_code": response["ranks_code"]}


if __name__ == "__main__":

    print(get_ranks("pkrf#728")["ranks"].__str__())