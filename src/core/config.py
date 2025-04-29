import json
import os
from cryptography.fernet import Fernet

class Config:
    def __init__(self):
        self.networks = {}
        self.dexs = {}
        self.private_key = None
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.load_config()

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                data = json.load(f)
                self.networks = data.get("networks", {})
                self.dexs = data.get("dexs", {})
                if data.get("private_key"):
                    self.private_key = self.cipher.decrypt(data["private_key"].encode()).decode()

    def add_network(self, name, rpc_url, chain_id):
        self.networks[name] = {"rpc_url": rpc_url, "chain_id": chain_id}
        self.save_config()

    def encrypt_private_key(self, private_key):
        self.private_key = private_key
        return self.cipher.encrypt(private_key.encode()).decode()

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump({
                "networks": self.networks,
                "dexs": self.dexs,
                "private_key": self.encrypt_private_key(self.private_key) if self.private_key else None
            }, f)
