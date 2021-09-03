import sqlite3


def getChannel(guild_id: int, channel: str) -> int:
    connection = sqlite3.connect('serverconfig/serverlogs.db')
    cursor = connection.cursor()
    check = cursor.execute(
        f"""SELECT {channel}
        FROM server_logs
        WHERE guild_id = {guild_id}""").fetchone()
    return check[0]


def innitiateGuild(guild_id: int) -> None:
    connection = sqlite3.connect('serverconfig/serverlogs.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO server_logs(guild_id, msg_delete, msg_edit, msg_pin, join_leave, kick_ban, channel, roles, user_change, scam)
        VALUES ({guild_id}, 0, 0, 0, 0, 0, 0, 0, 0, 0)""")
    connection.commit()


def deleteGuild(guild_id: int) -> None:
    connection = sqlite3.connect('serverconfig/serverlogs.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM server_logs
        WHERE guild_id = {guild_id}""")


def updateModule(guild_id: int, module: str, update: int) -> None:
    connection = sqlite3.connect('serverconfig/serverlogs.db')
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE server_logs
        SET {module} = {update}
        WHERE guild_id = {guild_id}""")
    connection.commit()
