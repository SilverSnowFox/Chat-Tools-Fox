import sqlite3

try:
    connection = sqlite3.connect('serverconfig/servermodules.db')
    cursor = connection.cursor()
except Exception:
    raise Exception

import sqlite3

try:
    connection = sqlite3.connect('serverconfig/serverchannels.db')
    cursor = connection.cursor()
except Exception:
    raise Exception


def getChannel(guild_id: int, channel: str) -> int:
    check = cursor.execute(
        f"""SELECT {channel}
        FROM server_channels
        WHERE guild_id = {guild_id}""").fetchone()
    return check[0]


def innitiateGuild(guild_id: int) -> None:
    cursor.execute(f"""
        INSERT INTO server_channels(guild_id, pins, pins_log, delete_edit, kicked_ban, join_leave, user_change, suggestions, reports)
        VALUES ({guild_id}, 0, 0, 0, 0, 0, 0, 0, 0)""")
    connection.commit()


def deleteGuild(guild_id: int) -> None:
    cursor.execute(f"""
        DELETE FROM server_channels
        WHERE guild_id = {guild_id}""")


def updateModule(guild_id: int, module: str, update: int) -> None:
    cursor.execute(f"""
        UPDATE server_channels
        SET {module} = {update}
        WHERE guild_id = {guild_id}""")
    connection.commit()
