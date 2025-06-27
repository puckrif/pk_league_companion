# Pk's League Companion

A Discord League of Legends companion bot  
! The bot is in french

## Commands

- *rank <riot_id> : Gives riot_id's currents ranks (SoloQ/DuoQ and Flex)
- *puck for a surprise
- *add <riot_id> : to track players and saves their ranks
- *remove <riot_id> : to delete a tracked players
- *saved : to show tracked players
- *clear : clears all saved players
- *history <riot_id> : to show a player's ranks history

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