import logging
import os
import json
import disnake
from art import text2art
from disnake.ext import commands
from src.utils.blacklist import is_blacklisted, check_user_on_main_server

logger = logging.getLogger(__name__)

GUILDS_FILE = "src/config/guilds.json"


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("H.", "h.", "!", "."),
            intents=disnake.Intents.all(),
        )
        self.remove_command('help')
        # Добавляем глобальную проверку перед каждой командой
        self.add_check(self.global_check)

    async def on_ready(self):
        print(text2art("EVIL", font="fire_font-s"))
        print("""
        [#] EVIL загружен
        [#] Разработчик: Cromwell | https://discord.gg/TCvsXj8teg
              """)
        logger.info(f"Вошёл в {self.user} (ID: {self.user.id})")

        await self.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.streaming,
                name="🔥 EVIL NUKE | discord.gg/TCvsXj8teg",
                url="https://www.twitch.tv/evil_nuke"
            ),
            status=disnake.Status.online
        )
        print("✅ Статус бота: Стримит 🔴")

        self.save_guilds()
        self.load_cogs()
        self.print_invite_link()

    def save_guilds(self):
        guild_ids = [str(guild.id) for guild in self.guilds]
        os.makedirs(os.path.dirname(GUILDS_FILE), exist_ok=True)
        with open(GUILDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(guild_ids, f, indent=2)
        logger.info(f"Сохранено {len(guild_ids)} серверов")

    def load_cogs(self):
        for filename in os.listdir("src/cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    self.load_extension(f"src.cogs.{filename[:-3]}")
                    logger.info(f"Ког {filename[:-3]} загружен!")
                except Exception as e:
                    logger.error(f"Ошибка загрузки кога {filename[:-3]}: {e}")

    def print_invite_link(self):
        permissions = disnake.Permissions(permissions=8)
        invite_link = disnake.utils.oauth_url(self.user.id, permissions=permissions)
        logger.info(f"Ссылка приглашения на бота: {invite_link}")

    async def on_guild_join(self, guild):
        self.save_guilds()
        logger.info(f"Добавлен на сервер: {guild.name} (ID: {guild.id})")

    async def on_guild_remove(self, guild):
        self.save_guilds()
        logger.info(f"Удалён с сервера: {guild.name} (ID: {guild.id})")

    # ============= ГЛОБАЛЬНАЯ ПРОВЕРКА (СРАБАТЫВАЕТ ДО ВЫПОЛНЕНИЯ КОМАНДЫ) =============
    async def global_check(self, ctx):
        """Проверка перед выполнением каждой команды (срабатывает ДО выполнения)"""
        # Пропускаем проверку для !ehelp
        if ctx.command and ctx.command.name in ["ehelp", "помощь", "commands"]:
            return True
        
        # Проверяем, что команда вызвана на сервере
        if ctx.guild is None:
            return True  # Разрешаем команды в ЛС
        
        # ===== ПРОВЕРКА: ПОЛЬЗОВАТЕЛЬ НА ГЛАВНОМ СЕРВЕРЕ =====
        if not check_user_on_main_server(ctx):
            embed = disnake.Embed(
                title="❌ Доступ запрещён",
                description="Вы не состоите на главном сервере!\n\n"
                            "Чтобы использовать команды бота, вы должны быть участником\n"
                            "сервера, который находится в чёрном списке.\n\n"
                            "💡 **Как получить доступ:**\n"
                            "1. заходите по [этой ссылке](https://discord.gg/TCvsXj8teg)\n"
                            "2. Зайдите на этот сервер\n"
                            "3. После этого вы сможете использовать команды здесь",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return False  # БЛОКИРУЕМ КОМАНДУ
        
        # ===== ПРОВЕРКА: ЧЁРНЫЙ СПИСОК (сервер, на котором вызывают команду) =====
        if ctx.guild and is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер находится в чёрном списке.\n"
                            "Команды бота недоступны здесь.\n"
                            "Доступна только команда `!ehelp`",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return False  # БЛОКИРУЕМ КОМАНДУ
        
        return True  # РАЗРЕШАЕМ КОМАНДУ