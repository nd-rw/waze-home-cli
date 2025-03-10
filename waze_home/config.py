"""Configuration for the Waze Home CLI."""

from pathlib import Path
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Default locations from CLAUDE.md
DEFAULT_LOCATIONS = {
    "home": "91 Abbett St, Scarborough WA 6019",
    "work": "11 Mount St, Perth WA 6000",
}

# Configuration directory
CONFIG_DIR = Path.home() / ".config" / "waze-home"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_config() -> Dict[str, Any]:
    """Get the configuration from the config file or environment variables."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    
    # Otherwise, use defaults or environment variables
    return {
        "locations": {
            "home": os.getenv("WAZE_HOME_LOCATION", DEFAULT_LOCATIONS["home"]),
            "work": os.getenv("WAZE_WORK_LOCATION", DEFAULT_LOCATIONS["work"]),
        },
        "waze_api_key": os.getenv("WAZE_API_KEY", ""),
    }

def save_config(config: Dict[str, Any]) -> None:
    """Save the configuration to the config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def set_location(name: str, address: str) -> None:
    """Set a location in the configuration."""
    config = get_config()
    config.setdefault("locations", {})
    config["locations"][name] = address
    save_config(config)

def get_location(name: str) -> str:
    """Get a location from the configuration."""
    config = get_config()
    return config.get("locations", {}).get(name, DEFAULT_LOCATIONS.get(name, ""))