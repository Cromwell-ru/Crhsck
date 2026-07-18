import disnake
from disnake.ext import commands
from ..utils.rich_presence import rich_presence


class PresenceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ALLOWED_USER_ID = 1354873565161324646  # Только твой ID

    async def check_owner(self, ctx):
        """Проверяет, является ли пользователь владельцем"""
        if ctx.author.id != self.ALLOWED_USER_ID:
            embed = disnake.Embed(
                title="❌ Доступ запрещён",
                description="У вас нет прав на использование этой команды.\n"
                            "Только владелец бота может управлять Presence.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return False
        return True

    @commands.command(name="presence_on")
    async def presence_on(self, ctx):
        """Включить Rich Presence (только владелец)"""
        if not await self.check_owner(ctx):
            return

        try:
            rich_presence.start()
            embed = disnake.Embed(
                title="✅ Rich Presence включён",
                description="Статус отображается в Discord.",
                color=disnake.Color.green()
            )
        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Не удалось включить: {e}",
                color=disnake.Color.red()
            )
        await ctx.send(embed=embed)

    @commands.command(name="presence_off")
    async def presence_off(self, ctx):
        """Выключить Rich Presence (только владелец)"""
        if not await self.check_owner(ctx):
            return

        try:
            rich_presence.stop()
            embed = disnake.Embed(
                title="✅ Rich Presence выключен",
                description="Статус скрыт.",
                color=disnake.Color.green()
            )
        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Не удалось выключить: {e}",
                color=disnake.Color.red()
            )
        await ctx.send(embed=embed)

    @commands.command(name="presence_set")
    async def presence_set(self, ctx, *, status: str):
        """Установить кастомный статус (только владелец)"""
        if not await self.check_owner(ctx):
            return

        try:
            rich_presence.set_custom(status, "EVIL NUKE BOT")
            embed = disnake.Embed(
                title="✅ Статус обновлён",
                description=f"Новый статус: **{status}**",
                color=disnake.Color.green()
            )
        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Не удалось обновить: {e}",
                color=disnake.Color.red()
            )
        await ctx.send(embed=embed)

    @commands.command(name="presence_inactive")
    async def presence_inactive(self, ctx):
        """Установить статус 'Не активен' (только владелец)"""
        if not await self.check_owner(ctx):
            return

        try:
            rich_presence.set_inactive()
            embed = disnake.Embed(
                title="✅ Статус обновлён",
                description="Статус: **Не активен**",
                color=disnake.Color.green()
            )
        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Не удалось обновить: {e}",
                color=disnake.Color.red()
            )
        await ctx.send(embed=embed)

    @commands.command(name="presence_full")
    async def presence_full(self, ctx):
        """Установить полный статус (только владелец)"""
        if not await self.check_owner(ctx):
            return

        try:
            rich_presence.set_full_presence()
            embed = disnake.Embed(
                title="✅ Полный статус установлен",
                description="Статус с кнопкой 'Присоединиться' активен.",
                color=disnake.Color.green()
            )
        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Не удалось установить: {e}",
                color=disnake.Color.red()
            )
        await ctx.send(embed=embed)


# ============= ЭТО ОБЯЗАТЕЛЬНО! =============
def setup(bot):
    bot.add_cog(PresenceCommands(bot))