import os
import datetime
import dotenv
import requests
from apps import puuid_fetcher

dotenv.load_dotenv()
riot_api_key = os.getenv("RIOT_API_KEY")

link = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-puuid/"


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

def get_ranks(riot_id):
    response = get_ranks_raw(riot_id)
    if response["ranks"] != None:
        ranks_raw = response["ranks"]
        ranks = {
                "date": datetime.datetime.now(),

                "solo":{
                    "tier": None,
                    "rank": None,
                    "leaguePoints": None
                },

                "flex":{
                    "tier": None,
                    "rank": None,
                    "leaguePoints": None
                }
            }
        
        for queue in ranks_raw :
            if queue["queueType"] == "RANKED_SOLO_5x5":
                ranks["solo"]["tier"] = queue["tier"]
                ranks["solo"]["rank"] = queue["rank"]
                ranks["solo"]["leaguePoints"] = queue["leaguePoints"]

            if queue["queueType"] == "RANKED_FLEX_SR":
                ranks["flex"]["tier"] = queue["tier"]
                ranks["flex"]["rank"] = queue["rank"]
                ranks["flex"]["leaguePoints"] = queue["leaguePoints"]
    else :
        ranks = None
    return {"ranks": ranks, "puuid_code": response["puuid_code"], "ranks_code": response["ranks_code"]}


if __name__ == "__main__":

    print(get_ranks("pkrf#728"))