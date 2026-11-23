"""
Unit tests for the Apple Sharing Module (apple_share.py).
"""

import pytest
from apple_share import AppleShareSession, invite_to_apple

def test_apple_share_session_init():
    """Test session initialization with default and custom apple types."""
    session_default = AppleShareSession()
    assert session_default.apple_type in AppleShareSession.SUPPORTED_APPLE_TYPES
    assert not session_default.is_sliced
    assert session_default.participants == ["Host"]

    session_custom = AppleShareSession("Honeycrisp")
    assert session_custom.apple_type == "Honeycrisp"

def test_accept_invitation():
    """Test participant joining the session."""
    session = AppleShareSession("Fuji")
    result = session.accept_invitation("Alice")
    
    assert result["status"] == "joined"
    assert "Alice" in result["participants"]
    assert result["apple_type"] == "Fuji"
    assert "Alice gladly joined" in result["message"]

    # Test duplicate or whitespace handling
    result_dup = session.accept_invitation("Alice")
    assert len(result_dup["participants"]) == 2  # Host + Alice

    result_empty = session.accept_invitation("   ")
    assert "Friend" in result_empty["participants"]

def test_slice_apple():
    """Test slicing the virtual apple."""
    session = AppleShareSession("Gala")
    result = session.slice_apple(4)
    
    assert result["status"] == "sliced"
    assert session.is_sliced is True
    assert session.slices_remaining == 4
    assert "4 juicy pieces" in result["message"]

    # Test zero or negative slice fallback
    session_zero = AppleShareSession()
    res_zero = session_zero.slice_apple(0)
    assert res_zero["slices_remaining"] == 1

def test_share_slice():
    """Test sharing slices with participants."""
    session = AppleShareSession("Pink Lady")
    
    # Try sharing before slicing
    err_result = session.share_slice("Bob")
    assert err_result["status"] == "error"

    # Slice and share
    session.slice_apple(2)
    share_res1 = session.share_slice("Bob")
    assert share_res1["status"] == "shared"
    assert share_res1["slices_remaining"] == 1

    share_res2 = session.share_slice("Charlie")
    assert share_res2["status"] == "shared"
    assert share_res2["slices_remaining"] == 0

    # Share when none left
    err_res2 = session.share_slice("Dave")
    assert err_res2["status"] == "error"

def test_invite_to_apple_helper():
    """Test top-level invitation response function."""
    prompt = "i am gonna eat an apple will you like to join me"
    response = invite_to_apple(prompt, "Sam")
    
    assert response["user_message"] == prompt
    assert response["join_session"]["status"] == "joined"
    assert "Sam" in response["join_session"]["participants"]
    assert response["slicing"]["status"] == "sliced"
    assert "🍎" in response["final_reply"]
