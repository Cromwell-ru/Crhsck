import json
import os
from datetime import datetime, timedelta

KEYS_FILE = "src/config/keys.json"


class KeyManager:
    def __init__(self):
        self.keys = {}
        self.load_keys()

    def load_keys(self):
        try:
            with open(KEYS_FILE, 'r', encoding='utf-8') as f:
                self.keys = json.load(f)
        except:
            self.keys = {}
            self.save_keys()

    def save_keys(self):
        os.makedirs(os.path.dirname(KEYS_FILE), exist_ok=True)
        with open(KEYS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.keys, f, indent=2, ensure_ascii=False)

    def add_key(self, key, expires_at=None):
        self.keys[key] = {
            "expires_at": expires_at,
            "used_by": None,
            "used_at": None
        }
        self.save_keys()

    def use_key(self, key, user_id):
        if key not in self.keys:
            return False, "❌ Ключ не найден"

        key_data = self.keys[key]

        if key_data.get("used_by") is not None and key_data.get("expires_at") is not None:
            return False, "❌ Ключ уже был использован"

        if key_data.get("expires_at") is not None:
            expires = datetime.fromisoformat(key_data["expires_at"])
            if datetime.now() > expires:
                return False, "❌ Срок действия ключа истёк"

        expires_at = (datetime.now() + timedelta(days=7)).isoformat()
        self.keys[key]["expires_at"] = expires_at
        self.keys[key]["used_by"] = str(user_id)
        self.keys[key]["used_at"] = datetime.now().isoformat()
        self.save_keys()
        return True, f"✅ Ключ активирован! Доступ к !vipnuke до {expires_at}"

    def has_access(self, user_id):
        for key, data in self.keys.items():
            if data.get("used_by") == str(user_id):
                if data.get("expires_at") is None:
                    return True
                try:
                    expires = datetime.fromisoformat(data["expires_at"])
                    if datetime.now() <= expires:
                        return True
                except:
                    pass
        return False

    def get_access_expiry(self, user_id):
        for key, data in self.keys.items():
            if data.get("used_by") == str(user_id):
                return data.get("expires_at")
        return None


key_manager = KeyManager()

# Бесконечный ключ
if "RVVS-8123-CRMWL-DESS" not in key_manager.keys:
    key_manager.add_key("RVVS-8123-CRMWL-DESS", expires_at=None)