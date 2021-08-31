import sqlite3

try:
    connection = sqlite3.connect('serverconfig/servermodules.db')
    cursor = connection.cursor()
except Exception:
    raise Exception


def getConfig(guild_id: int, module: str) -> bool:
    check = cursor.execute(
        f"""SELECT {module}
        FROM server_modules
        WHERE guild_id = {guild_id}""").fetchone()
    return bool(check[0])


def innitiateGuild(guild_id: int) -> None:
    cursor.execute(f"""
        INSERT INTO server_modules(guild_id, ghost_ping, anti_scam, msg_links, blacklisting)
        VALUES ({guild_id}, 1, 1, 1, 0)""")
    connection.commit()


def deleteGuild(guild_id: int) -> None:
    cursor.execute(f"""
        DELETE FROM server_modules
        WHERE guild_id = {guild_id}""")


def updateModule(guild_id: int, module: str, update: bool) -> None:
    cursor.execute(f"""
        UPDATE server_modules
        SET {module} = {int(update)}
        WHERE guild_id = {guild_id}""")
    connection.commit()
