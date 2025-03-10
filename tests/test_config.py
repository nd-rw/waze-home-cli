"""Tests for the config module."""

import pytest
from unittest.mock import patch, mock_open
import json
import os

from waze_home.config import (
    get_config,
    set_location,
    get_location,
    DEFAULT_LOCATIONS,
)


@pytest.fixture
def mock_config_file():
    """Fixture to mock config file operations."""
    config_data = {
        "locations": {
            "home": "Test Home Address",
            "work": "Test Work Address",
            "gym": "Test Gym Address",
        },
        "waze_api_key": "test_api_key",
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
        yield config_data


def test_get_config_with_existing_file(mock_config_file):
    """Test getting config when the config file exists."""
    with patch("waze_home.config.CONFIG_FILE.exists", return_value=True):
        config = get_config()
        
    assert config == mock_config_file
    assert config["locations"]["home"] == "Test Home Address"
    assert config["locations"]["work"] == "Test Work Address"


def test_get_config_with_no_file():
    """Test getting config when the config file does not exist."""
    with patch("waze_home.config.CONFIG_FILE.exists", return_value=False):
        with patch.dict(os.environ, {}, clear=True):
            config = get_config()
    
    assert "locations" in config
    assert config["locations"]["home"] == DEFAULT_LOCATIONS["home"]
    assert config["locations"]["work"] == DEFAULT_LOCATIONS["work"]


def test_get_config_with_env_vars():
    """Test getting config with environment variables set."""
    test_home = "Env Home Address"
    test_work = "Env Work Address"
    test_api_key = "env_api_key"
    
    with patch("waze_home.config.CONFIG_FILE.exists", return_value=False):
        with patch.dict(os.environ, {
            "WAZE_HOME_LOCATION": test_home,
            "WAZE_WORK_LOCATION": test_work,
            "WAZE_API_KEY": test_api_key,
        }):
            config = get_config()
    
    assert config["locations"]["home"] == test_home
    assert config["locations"]["work"] == test_work
    assert config["waze_api_key"] == test_api_key


def test_set_location():
    """Test setting a location."""
    with patch("waze_home.config.get_config") as mock_get_config:
        with patch("waze_home.config.save_config") as mock_save_config:
            mock_get_config.return_value = {
                "locations": {
                    "home": "Existing Home",
                    "work": "Existing Work",
                }
            }
            
            set_location("gym", "New Gym Address")
            
            expected_config = {
                "locations": {
                    "home": "Existing Home",
                    "work": "Existing Work",
                    "gym": "New Gym Address",
                }
            }
            
            mock_save_config.assert_called_once_with(expected_config)


def test_get_location_existing():
    """Test getting an existing location."""
    with patch("waze_home.config.get_config") as mock_get_config:
        mock_get_config.return_value = {
            "locations": {
                "home": "Test Home",
                "work": "Test Work",
            }
        }
        
        location = get_location("home")
        assert location == "Test Home"
        
        location = get_location("work")
        assert location == "Test Work"


def test_get_location_missing_with_default():
    """Test getting a missing location that has a default value."""
    # Remove the key from the config but it should fall back to DEFAULT_LOCATIONS
    with patch("waze_home.config.get_config") as mock_get_config:
        mock_get_config.return_value = {"locations": {}}
        
        location = get_location("home")
        assert location == DEFAULT_LOCATIONS["home"]


def test_get_location_missing_without_default():
    """Test getting a missing location without a default value."""
    with patch("waze_home.config.get_config") as mock_get_config:
        mock_get_config.return_value = {"locations": {}}
        
        location = get_location("gym")
        assert location == ""