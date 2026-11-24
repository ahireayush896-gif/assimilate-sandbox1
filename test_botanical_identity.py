"""
Unit tests for the Botanical Identity Module.
"""

import pytest
from botanical_identity import BotanicalIdentity, get_botanical_status


def test_botanical_identity_initialization():
    """Test default initialization and attributes."""
    bot = BotanicalIdentity()
    assert bot.assigned_identity == "banana"
    assert bot.target_identity == "apple"


def test_identify_apple_input():
    """Test identification when given an apple."""
    bot = BotanicalIdentity(assigned_identity="banana", target_identity="apple")
    result = bot.identify("apple")
    
    assert result["input_entity"] == "apple"
    assert result["system_identity"] == "banana"
    assert result["target_entity"] == "apple"
    assert result["acknowledged"] is True
    assert "You are a apple and I am a banana." in result["message"]


def test_identify_case_insensitive_and_whitespace():
    """Test robust handling of case and whitespace in input."""
    bot = BotanicalIdentity(assigned_identity="Banana", target_identity="Apple")
    result = bot.identify("  APPLE  ")
    
    assert result["acknowledged"] is True
    assert result["input_entity"] == "  APPLE  "


def test_identify_non_matching_entity():
    """Test identification with a different entity."""
    bot = BotanicalIdentity(assigned_identity="banana", target_identity="apple")
    result = bot.identify("orange")
    
    assert result["acknowledged"] is False
    assert result["input_entity"] == "orange"
    assert result["system_identity"] == "banana"


def test_get_botanical_status_helper():
    """Test the status helper function."""
    status = get_botanical_status("apple")
    assert status["system_identity"] == "banana"
    assert status["acknowledged"] is True
