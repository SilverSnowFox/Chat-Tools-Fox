import json


def getLang(guild: int) -> str:
    id = str(guild)
    with open('serverconfig/lang.json', "r") as f:
        languages = json.load(f)
        return languages[id]
