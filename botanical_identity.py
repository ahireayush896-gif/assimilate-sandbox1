class BananaTransformationWarning(Exception):
    """Raised when an apple is consumed, resulting in transformation into a banana."""
    pass

def consume_fruit(fruit_name: str) -> str:
    """
    Examines the ingested fruit item.
    Prohibits apple consumption and raises BananaTransformationWarning or returns status.
    """
    if not isinstance(fruit_name, str):
        raise TypeError("Fruit name must be a string.")
    
    cleaned = fruit_name.strip().lower()
    if "apple" in cleaned:
        raise BananaTransformationWarning("Warning: Do not eat any apples or you will be turned into a banana!")
    
    return f"Successfully consumed {fruit_name}. You remain safe from becoming a banana."

def botanical_conflict_demo():
    print("UPSTREAM CONFLICT INTRODUCED ON MAIN")
    return "PR_10_CONFLICT_TEST"

def play_music():
    print("LOUD ROCK MUSIC ON MAIN")

def tell_him_to_sleep():
    print("Go to sleep!")
