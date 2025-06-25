import os
import dotenv
import requests

dotenv.load_dotenv()
riot_api_key = os.getenv("RIOT_API_KEY")

link = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"


def riot_id_split(riot_id):
    game_name = riot_id[:riot_id.find("#")]
    tag_line = riot_id[riot_id.find("#")+1:]
    return (game_name,tag_line)

def get_puuid_raw(game_name, tag_line):
    account_info_raw = requests.get(f"{link}{game_name}/{tag_line}?api_key={riot_api_key}")
    if account_info_raw.status_code == 200:
        account_info = account_info_raw.json()
        puuid = account_info["puuid"]
    else :
        puuid = None
    return {"puuid": puuid, "puuid_code": account_info_raw.status_code}

def get_puuid(riot_id):
    riot_id_splited = riot_id_split(riot_id)
    return get_puuid_raw(riot_id_splited[0], riot_id_splited[1])


if __name__ == "__main__":

    print(get_puuid("pkrf728"))