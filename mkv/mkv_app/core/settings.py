import os
import json
import logging
from PyQt6.QtCore import QSettings, QStandardPaths

class AppSettings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppSettings, cls).__new__(cls)
            cls._instance._init_settings()
        return cls._instance

    def _init_settings(self):
        self.app_name = "mkvBatch"
        self.app_data_path = os.path.join(os.getenv("APPDATA"), self.app_name)
        self.config_file = os.path.join(self.app_data_path, "config.json")
        
        # Defaults
        self.defaults = {
            "mkvtoolnix": "C:\\Program Files\\MKVToolNix",
            "languageCodes": ["en", "de"]
        }
        
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.app_data_path):
            try:
                os.makedirs(self.app_data_path)
            except OSError as e:
                logging.error(f"Failed to create app data directory: {e}")
                return self.defaults.copy()

        if not os.path.exists(self.config_file):
            self.save_config(self.defaults)
            return self.defaults.copy()

        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            return self.defaults.copy()

    def save_config(self, config=None):
        if config:
            self.config = config
        
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default if default is not None else self.defaults.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    @property
    def mkvmerge_path(self):
        return os.path.join(self.get("mkvtoolnix"), "mkvmerge.exe")

    @property
    def mkvpropedit_path(self):
        return os.path.join(self.get("mkvtoolnix"), "mkvpropedit.exe")
