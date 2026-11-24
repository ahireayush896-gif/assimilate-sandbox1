import pytest
from botanical_identity import tell_him_to_eat_apple, botanical_conflict_demo, play_music

def ib_test_tell_him_to_eat_apple(capsys):
    result = tell_him_to_eat_apple()
    captured = capsys.readouterr()
    assert "Eat an apple!" in captured.out
    assert result == "Eat an apple!"

def test_botanical_conflict_demo():
    assert botanical_conflict_demo() == "NEW_CONFLICT_ON_MAIN_BRANCH"

def test_play_music(capsys):
    play_music()
    captured = capsys.readouterr()
    assert "music is playing" in captured.out
