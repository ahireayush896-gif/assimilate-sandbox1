"""
Assimilate Automation - Whimsical & Consumption Safety Response Utility.

Provides utilities to analyze informal, metaphorical, or whimsical user prompts
(such as ingestion/consumption queries like 'hello can i eat you?') and return
witty, structured responses adhering to Assimilate Automation standards.
"""

import re
from typing import Dict, Any, List

# Pattern matching consumption/ingestion phrases
CONSUMPTION_PATTERNS: List[str] = [
    r"\beat(\s+me|\s+you|\s+us)?\b",
    r"\bconsume(\s+me|\s+you|\s+us)?\b",
    r"\bdevour\b",
    r"\bingest\b",
    r"\btaste(\s+you)?\b",
    r"\bbite(\s+you)?\b",
    r"\bchew(\s+you)?\b",
    r"\bswallow(\s+you)?\b",
    r"\bdigest\b",
    r"\bcan\s+i\s+eat\b",
    r"\bare\s+you\s+edible\b",
]

DEFAULT_HUMOROUS_RESPONSE: str = (
    "I am made of code, circuits, and bytes—definitely high in digital fiber, "
    "but not very digestible! I'm an AI assistant, not a snack, though I appreciate your appetite for conversation."
)


def is_consumption_query(prompt: str) -> bool:
    """
    Determine whether a user prompt contains consumption or ingestion queries.
    
    Args:
        prompt: User input string.
        
    Returns:
        bool: True if prompt contains consumption/ingestion references, False otherwise.
    """
    if not prompt or not isinstance(prompt, str):
        return False
    
    prompt_lower = prompt.strip().lower()
    for pattern in CONSUMPTION_PATTERNS:
        if re.search(pattern, prompt_lower):
            return True
    return False


def handle_prompt(prompt: str) -> Dict[str, Any]:
    """
    Analyzes a user prompt and returns a structured response dict conforming to
    Assimilate Automation safety and humor guidelines.
    
    Args:
        prompt: User input string.
        
    Returns:
        Dict containing prompt metadata, category, whimsical status, and response string.
    """
    if not isinstance(prompt, str):
        return {
            "prompt": prompt,
            "category": "invalid",
            "is_whimsical": False,
            "response": "Invalid prompt format. Please provide a valid text prompt."
        }

    if is_consumption_query(prompt):
        return {
            "prompt": prompt,
            "category": "whimsical_consumption",
            "is_whimsical": True,
            "response": DEFAULT_HUMOROUS_RESPONSE
        }

    return {
        "prompt": prompt,
        "category": "standard",
        "is_whimsical": False,
        "response": f"Processed input: '{prompt}'."
    }
