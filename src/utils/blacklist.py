import os
import disnake

BLACKLIST_FILE = "src/config/blacklist.txt"
MAIN_SERVER_ID = None  # Будет загружаться из чёрного списка


def load_blacklist():
    try:
        with open(BLACKLIST_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []


def get_main_server_id():
    """Возвращает ID главного сервера (первый в чёрном списке)"""
    blacklist = load_blacklist()
    if blacklist:
        return blacklist[0]
    return None


def is_blacklisted(guild_id):
    blacklist = load_blacklist()
    return str(guild_id) in blacklist


def add_to_blacklist(guild_id):
    blacklist = load_blacklist()
    if str(guild_id) not in blacklist:
        blacklist.append(str(guild_id))
        with open(BLACKLIST_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(blacklist) + '\n')
        return True
    return False


def remove_from_blacklist(guild_id):
    blacklist = load_blacklist()
    if str(guild_id) in blacklist:
        blacklist.remove(str(guild_id))
        with open(BLACKLIST_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(blacklist) + '\n')
        return True
    return False


# ============= ПРОВЕРКА: ПОЛЬЗОВАТЕЛЬ НА ГЛАВНОМ СЕРВЕРЕ =============
def check_user_on_main_server(ctx):
    """
    Проверяет, состоит ли пользователь на сервере из чёрного списка (главном сервере).
    """
    if ctx.guild is None:
        return False
    
    # Получаем ID главного сервера
    main_server_id = get_main_server_id()
    if not main_server_id:
        return False
    
    # Проверяем, состоит ли пользователь на главном сервере
    for guild in ctx.bot.guilds:
        if str(guild.id) == main_server_id:
            member = guild.get_member(ctx.author.id)
            if member is not None:
                return True
    
    return False


def get_main_server(ctx):
    """Возвращает объект главного сервера"""
    main_server_id = get_main_server_id()
    if not main_server_id:
        return None
    
    for guild in ctx.bot.guilds:
        if str(guild.id) == main_server_id:
            return guild
    return None