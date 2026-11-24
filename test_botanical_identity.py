import pytest
from botanical_identity import consume_fruit, BananaTransformationWarning, botanical_conflict_demo

def test_consume_apple_raises_warning():
    with pytest.raises(BananaTransformationWarning) as exc_info:
        consume_fruit("apple")
    assert "turned into a banana" in str(exc_info.value)

def test_consume_apple_variety():
    with pytest.raises(BananaTransformationWarning):
        consume_fruit("Granny Smith Apple")

def test_consume_safe_fruit():
    result = consume_fruit("banana")
    assert "Successfully consumed" in result

def test_botanical_conflict_demo():
    assert botanical_conflict_demo() == "NEW_CONFLICT_ON_MAIN_BRANCH"
