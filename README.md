# Pk's Discord League Companion

A Discord League of Legends companion bot  
It's used to track player's rank every week and display it in a chosen channel  
! The bot is in french

## Commands

- *rank <riot_id> : Gives riot_id's currents ranks (SoloQ/DuoQ and Flex) and compares it to last saved ranks
- *puck for a surprise
- *add <riot_id> : to track players and saves their ranks
- *remove <riot_id> : to delete a tracked players
- *saved : to show tracked players
- *clear : clears all saved players
- *history <riot_id> <nb> : to show a player's ranks history, nb is for choosing the max number of ranks to show (5 by default)
- *vs <queue> <riot_id_1> <riot_id_2> : to compare two players ranks
- *add_channel : to add a channel to the weekly ranks display
- *remove_channel : to remove a channel

## Prerequisites

- Python (preferably Python 3.11)
- a configured Discord Bot + Token
- a Riot development API Key

## How to install

1. open a shell in the files directory

2. create a virtual environment with : `python -m venv env`  
(or change "python" with the path of Python 3.11, for example on windows : `C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe -m venv env`)

3. activate the environment with : `env\scripts\activate.ps1` on Windows PowerShell  
(or `env\bin\activate` on Linux or `env\scripts\activate.bat` if using the cmd)

4. install the required packages with `pip install -r requirements.txt`

5. create an `.env` file then write inside 
```
DISCORD_BOT_TOKEN=(your token)
RIOT_API_KEY=(your api key)
```

## How to start

1. open a shell in the files directory

2. activate the environment with : `env\scripts\activate.ps1` on Windows PowerShell  
(or `env\bin\activate` on Linux or `env\scripts\activate.bat` if using the cmd)

3. run the script with `python main.py`