import sqlite3


def getChannel(guild_id: int, channel: str) -> int:
    connection = sqlite3.connect('serverconfig/serverchannels.db')
    cursor = connection.cursor()
    check = cursor.execute(
        f"""SELECT {channel}
        FROM server_channels
        WHERE guild_id = {guild_id}""").fetchone()
    connection.close()
    return check[0]


def innitiateGuild(guild_id: int) -> None:
    connection = sqlite3.connect('serverconfig/serverchannels.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO server_channels(guild_id, pins, suggestions, reports)
        VALUES ({guild_id}, 0, 0, 0)""")
    connection.commit()
    connection.close()


def deleteGuild(guild_id: int) -> None:
    connection = sqlite3.connect('serverconfig/serverchannels.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM server_channels
        WHERE guild_id = {guild_id}""")
    connection.close()


def updateModule(guild_id: int, module: str, update: int) -> None:
    connection = sqlite3.connect('serverconfig/serverchannels.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE server_channels
        SET {module} = {update}
        WHERE guild_id = {guild_id}""")
    connection.commit()
    connection.close()
