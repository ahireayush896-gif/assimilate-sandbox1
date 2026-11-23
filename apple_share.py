"""
Apple Sharing Core Module
Simulates an interactive apple-sharing session with friends or AI companions.
"""

import random
from typing import Dict, Any, Optional

class AppleShareSession:
    """Manages a virtual apple-sharing session."""
    
    SUPPORTED_APPLE_TYPES = ["Honeycrisp", "Fuji", "Granny Smith", "Gala", "Pink Lady"]
    
    def __init__(self, apple_type: Optional[str] = None):
        self.apple_type = apple_type or random.choice(self.SUPPORTED_APPLE_TYPES)
        self.is_sliced = False
        self.slices_remaining = 0
        self.participants = ["Host"]

    def accept_invitation(self, friend_name: str = "Friend") -> Dict[str, Any]:
        """Accepts an invitation to join the apple-sharing session."""
        if not friend_name or not friend_name.strip():
            friend_name = "Friend"
        
        friend_name = friend_name.strip()
        if friend_name not in self.participants:
            self.participants.append(friend_name)
            
        return {
            "status": "joined",
            "message": f"Yay! {friend_name} gladly joined the apple-sharing session! We are sharing a delicious {self.apple_type} apple.",
            "participants": self.participants,
            "apple_type": self.apple_type
        }

    def slice_apple(self, num_slices: int = 2) -> Dict[str, Any]:
        """Slices the virtual apple into shares."""
        if num_slices < 1:
            num_slices = 1
        
        self.is_sliced = True
        self.slices_remaining = num_slices
        
        return {
            "status": "sliced",
            "message": f"The {self.apple_type} apple has been sliced into {num_slices} juicy pieces!",
            "slices_remaining": self.slices_remaining
        }

    def share_slice(self, recipient: str) -> Dict[str, Any]:
        """Shares a slice with a participant."""
        if not self.is_sliced or self.slices_remaining <= 0:
            return {
                "status": "error",
                "message": "The apple hasn't been sliced yet or no slices are left!"
            }
        
        self.slices_remaining -= 1
        return {
            "status": "shared",
            "message": f"Handed a crunchy slice of {self.apple_type} apple to {recipient}. Enjoy!",
            "slices_remaining": self.slices_remaining
        }


def invite_to_apple(user_message: str, friend_name: str = "Friend") -> Dict[str, Any]:
    """
    Responds to an apple-sharing invitation message like 'i am gonna eat an apple will you like to join me'.
    """
    session = AppleShareSession()
    join_response = session.accept_invitation(friend_name)
    slice_response = session.slice_apple(2)
    
    return {
        "user_message": user_message,
        "join_session": join_response,
        "slicing": slice_response,
        "final_reply": f"I would love to join you! Nothing beats sharing a crisp {session.apple_type} apple together. 🍎✨"
    }


if __name__ == "__main__":
    result = invite_to_apple("i am gonna eat an apple will you like to join me", "Developer")
    print(result["final_reply"])
    print(result["join_session"]["message"])
    print(result["slicing"]["message"])
