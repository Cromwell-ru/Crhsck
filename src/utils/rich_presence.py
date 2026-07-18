import time
from pypresence import Presence
import threading
import logging
import sys

logger = logging.getLogger(__name__)


class RichPresence:
    def __init__(self, client_id="1527634058148974792"):
        self.client_id = client_id
        self.rpc = None
        self.running = False
        self.thread = None
        self.invite_url = "https://discord.gg/TCvsXj8teg"
        self.pipe = 0  # 0 - обычный Discord, 1 - Discord Canary, 2 - Discord PTB

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("✅ Rich Presence запущен")

    def stop(self):
        self.running = False
        if self.rpc:
            try:
                self.rpc.clear()
                self.rpc.close()
            except:
                pass
        print("⏹️ Rich Presence остановлен")

    def _run(self):
        """Основной цикл Rich Presence с обработкой ошибок"""
        try:
            # СПОСОБ 1: Указываем pipe и пробуем несколько вариантов
            pipes = [0, 1, 2]  # 0 - Discord, 1 - Canary, 2 - PTB
            
            for pipe in pipes:
                try:
                    print(f"🔄 Пробуем подключиться через pipe {pipe}...")
                    self.rpc = Presence(client_id=self.client_id, pipe=pipe)
                    self.rpc.connect()
                    self.pipe = pipe
                    print(f"✅ Подключение к Discord RPC установлено (pipe {pipe})")
                    break
                except Exception as e:
                    print(f"❌ Pipe {pipe} не работает: {e}")
                    continue
            
            if not self.rpc:
                print("❌ Не удалось подключиться через все pipes")
                return

            # Устанавливаем статус
            self.set_inactive()

            while self.running:
                time.sleep(15)

        except Exception as e:
            print(f"❌ Ошибка Rich Presence: {e}")
            logger.error(f"Rich Presence ошибка: {e}")
        finally:
            if self.rpc:
                try:
                    self.rpc.clear()
                    self.rpc.close()
                except:
                    pass

    def update(self, state=None, details=None, **kwargs):
        """Обновляет статус в Discord"""
        try:
            data = {}
            if state:
                data["state"] = state
            if details:
                data["details"] = details
            data.update(kwargs)
            
            # СПОСОБ 2: clear перед update
            self.rpc.clear()
            self.rpc.update(**data)
            print(f"📌 Статус обновлён: {state}")
        except Exception as e:
            print(f"❌ Ошибка обновления Presence: {e}")

    def set_inactive(self):
        """Устанавливает статус 'не активен' с кнопкой"""
        try:
            # СПОСОБ 2: clear перед update
            self.rpc.clear()
            self.rpc.update(
                state="Не активен",
                details="Ожидание...",
                large_image="ima3454354353ge_3_",
                large_text="EVIL",
                buttons=[
                    {"label": "🚀 Присоединиться", "url": self.invite_url}
                ]
            )
            print("📌 Статус установлен: Не активен (с кнопкой)")
        except Exception as e:
            print(f"❌ Ошибка установки статуса: {e}")

    def set_custom(self, state, details, large_image=None, large_text=None):
        """Устанавливает кастомный статус с кнопкой"""
        try:
            data = {
                "state": state,
                "details": details,
                "buttons": [
                    {"label": "🚀 Присоединиться", "url": self.invite_url}
                ]
            }
            if large_image:
                data["large_image"] = large_image
            if large_text:
                data["large_text"] = large_text

            self.rpc.clear()
            self.rpc.update(**data)
            print(f"📌 Статус обновлён: {state}")
        except Exception as e:
            print(f"❌ Ошибка установки кастомного статуса: {e}")

    def set_full_presence(self):
        """Полный статус с кнопкой"""
        try:
            self.rpc.clear()
            self.rpc.update(
                state="EVIL | Присоединяйся к нам",
                details="EVIL | Prime Desochka and Onix",
                start=1507665886,
                end=1507665886,
                large_image="ima3454354353ge_3_",
                large_text="EVIL",
                small_image="ima3454354353ge_3_",
                small_text="Rogue - Level 1000",
                party_id="ae488379-351d-4a4f-ad32-2b9b01c91657",
                party_size=[1259, 4300],
                join="MTI4NzM0OjFpMmhuZToxMjMxMjM=",
                buttons=[
                    {"label": "🚀 Присоединиться", "url": self.invite_url}
                ]
            )
            print("📌 Полный статус установлен с кнопкой")
        except Exception as e:
            print(f"❌ Ошибка установки полного статуса: {e}")


# Глобальный экземпляр
rich_presence = RichPresence()