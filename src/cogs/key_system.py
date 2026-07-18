import disnake
from disnake.ext import commands
from ..utils.key_manager import key_manager
from datetime import datetime, timedelta
import random
import string


class KeySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ============= АКТИВАЦИЯ КЛЮЧА (в ЛС) =============
    @commands.slash_command(name="key", description="Активировать ключ для доступа к !vipnuke")
    async def key(self, interaction: disnake.ApplicationCommandInteraction, key: str):
        # === ДЕФЕР (чтобы не было таймаута) ===
        await interaction.response.defer(ephemeral=True)

        if interaction.guild is not None:
            embed = disnake.Embed(
                title="❌ Ошибка",
                description="Эта команда доступна только в личных сообщениях!",
                color=disnake.Color.red()
            )
            await interaction.edit_original_response(embed=embed)
            return

        success, message = key_manager.use_key(key, interaction.author.id)

        embed = disnake.Embed(
            title="🔑 Активация ключа",
            description=message,
            color=disnake.Color.from_rgb(48, 49, 54) if success else disnake.Color.red()
        )

        if success:
            embed.add_field(
                name="💡 Команда",
                value="`!vipnuke`",
                inline=False
            )

        await interaction.edit_original_response(embed=embed)

    # ============= ГЕНЕРАЦИЯ КЛЮЧА (ТОЛЬКО ДЛЯ КОНКРЕТНОГО ID) =============
    @commands.slash_command(name="generate_key", description="Сгенерировать новый ключ")
    async def generate_key(self, interaction: disnake.ApplicationCommandInteraction, days: int = 7):
        # === ДЕФЕР ===
        await interaction.response.defer(ephemeral=True)

        ALLOWED_USER_ID = 1354873565161324646

        if interaction.author.id != ALLOWED_USER_ID:
            embed = disnake.Embed(
                title="❌ Доступ запрещён",
                description="У вас нет прав на использование этой команды.\n"
                            "Только владелец бота может генерировать ключи.",
                color=disnake.Color.red()
            )
            await interaction.edit_original_response(embed=embed)
            return

        # Генерируем ключ
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        key = f"{key[:4]}-{key[4:8]}-{key[8:12]}-{key[12:16]}"

        expires_at = (datetime.now() + timedelta(days=days)).isoformat()
        key_manager.add_key(key, expires_at)

        embed = disnake.Embed(
            title="✅ Ключ создан",
            description=f"Ключ: `{key}`\nДействует: {days} дней",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await interaction.edit_original_response(embed=embed)

    # ============= СПИСОК VIP-ПОЛЬЗОВАТЕЛЕЙ (ТОЛЬКО ДЛЯ КОНКРЕТНОГО ID) =============
    @commands.slash_command(name="vip_list", description="Список пользователей с VIP-доступом")
    async def vip_list(self, interaction: disnake.ApplicationCommandInteraction):
        # === ДЕФЕР ===
        await interaction.response.defer(ephemeral=True)

        ALLOWED_USER_ID = 1354873565161324646

        if interaction.author.id != ALLOWED_USER_ID:
            embed = disnake.Embed(
                title="❌ Доступ запрещён",
                description="У вас нет прав на использование этой команды.\n"
                            "Только владелец бота может просматривать VIP-список.",
                color=disnake.Color.red()
            )
            await interaction.edit_original_response(embed=embed)
            return

        vip_users = []
        for key, data in key_manager.keys.items():
            if data.get("used_by"):
                expires = data.get("expires_at")
                if expires is None:
                    vip_users.append({
                        "user_id": data["used_by"],
                        "expires": "Бессрочно"
                    })
                else:
                    try:
                        expires_dt = datetime.fromisoformat(expires)
                        if datetime.now() <= expires_dt:
                            vip_users.append({
                                "user_id": data["used_by"],
                                "expires": expires_dt.strftime("%Y-%m-%d %H:%M:%S")
                            })
                    except:
                        pass

        if not vip_users:
            embed = disnake.Embed(
                title="📋 VIP-пользователи",
                description="Нет активных VIP-пользователей",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            await interaction.edit_original_response(embed=embed)
            return

        description = ""
        for user in vip_users:
            try:
                user_obj = await self.bot.fetch_user(int(user["user_id"]))
                name = user_obj.name if user_obj else user["user_id"]
            except:
                name = user["user_id"]
            description += f"• {name} — {user['expires']}\n"

        embed = disnake.Embed(
            title="📋 VIP-пользователи",
            description=description,
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await interaction.edit_original_response(embed=embed)


def setup(bot):
    bot.add_cog(KeySystem(bot))