"""utils.py

Module provides a function to retrieve configuration values
"""

from pathlib import Path
import json


def get_config_value(key: str) -> str:
    """Retrieve a value from the config.json file by key.

    Args:
        key: The name of the config key to retrieve.

    Returns:
        The corresponding value as a string, or an empty string
        if the key is not found or an error occurs.
    """
    config_path = Path(__file__).resolve().parent / "config.json"
    try:
        with config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
        return config.get(key, "")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return ""
