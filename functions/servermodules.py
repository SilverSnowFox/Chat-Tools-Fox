import sqlite3


def getConfig(guild_id: int, module: str) -> bool:
    """Gets the server configuration"""

    with sqlite3.connect('serverconfig/servermodules.db') as connection:
        cursor = connection.cursor()
        check = cursor.execute(
            f"""SELECT {module}
            FROM server_modules
            WHERE guild_id = {guild_id}""").fetchone()
        return bool(check[0])


def innitiateGuild(guild_id: int) -> None:
    """Creates the guild entry"""

    with sqlite3.connect('serverconfig/servermodules.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
            INSERT INTO server_modules(guild_id, ghost_ping, anti_scam, msg_links, blacklisting)
            VALUES ({guild_id}, 1, 1, 1, 0)""")
        connection.commit()


def deleteGuild(guild_id: int) -> None:
    """Deletes the guild entry"""

    with sqlite3.connect('serverconfig/servermodules.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
            DELETE FROM server_modules
            WHERE guild_id = {guild_id}""")


def updateModule(guild_id: int, module: str, update: bool) -> None:
    """Updates a channel"""

    with sqlite3.connect('serverconfig/servermodules.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
            UPDATE server_modules
            SET {module} = {int(update)}
            WHERE guild_id = {guild_id}""")
        connection.commit()
