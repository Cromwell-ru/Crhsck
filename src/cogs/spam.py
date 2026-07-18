import disnake
import random
import asyncio
from disnake.ext import commands
from disnake.ext.commands import BucketType, CommandOnCooldown


class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spam")
    @commands.cooldown(1, 14400, BucketType.user)  # 4 часа
    async def spam(self, ctx, user: disnake.Member = None):
        """Спам в ЛС пользователя (5 случайных сообщений)"""
        if user is None:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Укажите пользователя: `!spam @user`",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        if user.bot:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Нельзя спамить ботам!",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        messages = [
            "Привет! Как дела? 😊 https://discord.gg/TCvsXj8teg",
            "Ты крутой! 🔥 https://discord.gg/TCvsXj8teg",
            "Заходи на наш сервер: https://discord.gg/TCvsXj8teg",
            "EVIL NUKE BOT 👑 https://discord.gg/TCvsXj8teg",
            "Спам-атака! 💀 https://discord.gg/TCvsXj8teg",
            "Ты попал под раздачу! 🎯 https://discord.gg/TCvsXj8teg",
            "EVIL - лучший бот для краша! 🚀 https://discord.gg/TCvsXj8teg",
            "Не забудь подписаться на нас! ❤️ https://discord.gg/TCvsXj8teg",
            "🔥 EVIL NUKE 🔥 https://discord.gg/TCvsXj8teg ",
            "Discord сервер: https://discord.gg/TCvsXj8teg"
        ]

        random_messages = random.sample(messages, 5)

        embed_start = disnake.Embed(
            title="📨 СПАМ ЗАПУЩЕН",
            description=f"**{ctx.author.name}** начал спам-атаку на **{user.name}**",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_start)

        try:
            for msg in random_messages:
                await user.send(msg)
                await asyncio.sleep(0.5)  # ← ЗАДЕРЖКА 0.5 СЕКУНДЫ

            embed_success = disnake.Embed(
                title="✅ СПАМ ЗАВЕРШЁН",
                description=f"**{user.name}** получил 5 сообщений от **{ctx.author.name}**",
                color=disnake.Color.green()
            )
            await ctx.send(embed=embed_success)

        except Exception as e:
            embed_error = disnake.Embed(
                title="❌ Ошибка",
                description=f"Не удалось отправить сообщения пользователю `{user.name}`.\n"
                            f"Возможно, у него закрыты ЛС.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed_error)

    @spam.error
    async def spam_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            hours = int(error.retry_after // 3600)
            minutes = int((error.retry_after % 3600) // 60)
            embed = disnake.Embed(
                title="⏳ Кулдаун",
                description=f"Команда на кулдауне. Повторите через **{hours} ч {minutes} мин**.",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            await ctx.send(embed=embed)
        else:
            raise error


def setup(bot):
    bot.add_cog(Spam(bot))