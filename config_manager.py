import sys
import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.default_config = {
            "scan_depth": 3,
            "auto_delete_threats": False,
            "log_level": "INFO"
        }

    def load_config(self) -> dict:
        if not self.config_file.exists():
            self.save_config(self.default_config)
            return self.default_config
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return self.default_config

    def save_config(self, config_data: dict) -> None:
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)

if __name__ == "__main__":
    manager = ConfigManager()
    cfg = manager.load_config()
    print(f"[*] Current configuration: {cfg}")