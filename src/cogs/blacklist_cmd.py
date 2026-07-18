import disnake
from disnake.ext import commands
from ..utils.blacklist import add_to_blacklist, remove_from_blacklist, load_blacklist


class BlacklistCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="blacklist_add")
    async def blacklist_add(self, ctx, guild_id: str):
        """Добавить сервер в чёрный список (только владелец)"""
        if add_to_blacklist(guild_id):
            embed = disnake.Embed(
                title="✅ Добавлено",
                description=f"Сервер `{guild_id}` добавлен в чёрный список.",
                color=disnake.Color.green()
            )
        else:
            embed = disnake.Embed(
                title="⚠️ Уже есть",
                description=f"Сервер `{guild_id}` уже в чёрном списке.",
                color=disnake.Color.orange()
            )
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="blacklist_remove")
    async def blacklist_remove(self, ctx, guild_id: str):
        """Удалить сервер из чёрного списка (только владелец)"""
        if remove_from_blacklist(guild_id):
            embed = disnake.Embed(
                title="✅ Удалено",
                description=f"Сервер `{guild_id}` удалён из чёрного списка.",
                color=disnake.Color.green()
            )
        else:
            embed = disnake.Embed(
                title="⚠️ Не найдено",
                description=f"Сервер `{guild_id}` не найден в чёрном списке.",
                color=disnake.Color.orange()
            )
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="blacklist_list")
    async def blacklist_list(self, ctx):
        """Показать чёрный список (только владелец)"""
        blacklist = load_blacklist()
        if not blacklist:
            embed = disnake.Embed(
                title="📋 Чёрный список",
                description="Чёрный список пуст.",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
        else:
            embed = disnake.Embed(
                title="📋 Чёрный список",
                description="\n".join([f"`{gid}`" for gid in blacklist]),
                color=disnake.Color.from_rgb(48, 49, 54)
            )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BlacklistCommands(bot))