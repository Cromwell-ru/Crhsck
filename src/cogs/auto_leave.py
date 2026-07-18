from disnake.ext import commands, tasks
from ..utils.blacklist import load_blacklist


class Autoleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leave_task.start()

    @tasks.loop(hours=4)  # Проверка каждые 4 часа
    async def leave_task(self):
        """Автоматический выход с серверов, которых нет в чёрном списке"""
        blacklist = load_blacklist()
        
        for guild in self.bot.guilds:
            # Проверяем, есть ли сервер в чёрном списке
            if str(guild.id) not in blacklist:
                try:
                    await guild.leave()
                    print(f"🚪 Бот вышел с сервера: {guild.name} (ID: {guild.id})")
                except Exception as e:
                    print(f"❌ Ошибка выхода с {guild.name}: {e}")
            else:
                print(f"⏳ Сервер {guild.name} (ID: {guild.id}) в чёрном списке — пропускаем")

    @leave_task.before_loop
    async def before_leave_task(self):
        """Ждём, пока бот запустится"""
        await self.bot.wait_until_ready()

    @commands.is_owner()
    @commands.command(name="autoleave_on")
    async def autoleave_on(self, ctx):
        """Включить автоливер (только владелец)"""
        if self.leave_task.is_running():
            embed = disnake.Embed(
                title="⚠️ Уже включён",
                description="Автоливер уже работает.",
                color=disnake.Color.orange()
            )
        else:
            self.leave_task.start()
            embed = disnake.Embed(
                title="✅ Автоливер включён",
                description="Бот будет автоматически выходить с серверов каждые 4 часа.\n"
                            "Сервера из чёрного списка будут пропущены.",
                color=disnake.Color.green()
            )
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="autoleave_off")
    async def autoleave_off(self, ctx):
        """Выключить автоливер (только владелец)"""
        if self.leave_task.is_running():
            self.leave_task.stop()
            embed = disnake.Embed(
                title="✅ Автоливер выключен",
                description="Бот больше не будет автоматически выходить с серверов.",
                color=disnake.Color.green()
            )
        else:
            embed = disnake.Embed(
                title="⚠️ Уже выключен",
                description="Автоливер уже отключён.",
                color=disnake.Color.orange()
            )
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(name="autoleave_status")
    async def autoleave_status(self, ctx):
        """Показать статус автоливера (только владелец)"""
        status = "🟢 Включён" if self.leave_task.is_running() else "🔴 Выключен"
        interval = self.leave_task.seconds if hasattr(self.leave_task, 'seconds') else "4 часа"
        
        blacklist = load_blacklist()
        
        embed = disnake.Embed(
            title="📊 Статус автоливера",
            description=f"**Статус:** {status}\n"
                        f"**Интервал:** {interval}\n"
                        f"**Серверов в чёрном списке:** {len(blacklist)}",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Autoleave(bot))