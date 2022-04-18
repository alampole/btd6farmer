"""
...
"""
from bot import Bot

statDict = {
    "Current_Round": None,
    "Last_Upgraded": None,
    "Last_Target_Change": None,
    "Last_Placement": None,
    "Uptime": 0
}

def main():
    # load config.json
    _config = {}

    btd_instance = Bot(config=_config)
    btd_instance.run()

if __name__ == "__main__":
    main()