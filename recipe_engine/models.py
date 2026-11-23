from dataclasses import dataclass, field
from typing import List, Optional, Set

@dataclass
class Ingredient:
    name: str
    amount: float
    unit: str  # e.g., 'grams', 'cups', 'pcs', 'tbsp', 'ml'

    def __post_init__(self):
        self.name = self.name.strip().lower()
        if self.amount < 0:
            raise ValueError(f"Ingredient amount for '{self.name}' cannot be negative.")

@dataclass
class Recipe:
    id: str
    title: str
    prep_time_minutes: int
    ingredients: List[Ingredient]
    instructions: List[str]
    dietary_tags: Set[str] = field(default_factory=set)  # e.g., 'vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'keto'
    calories: Optional[int] = None
    protein_grams: Optional[float] = None
    carbs_grams: Optional[float] = None
    fat_grams: Optional[float] = None

    def __post_init__(self):
        self.title = self.title.strip()
        if self.prep_time_minutes < 0:
            raise ValueError(f"Prep time for recipe '{self.title}' cannot be negative.")
        # Normalize dietary tags to lowercase
        self.dietary_tags = {tag.strip().lower() for tag in self.dietary_tags}

@dataclass
class UserPreferences:
    dietary_restrictions: Set[str] = field(default_factory=set)
    max_prep_time_minutes: Optional[int] = None
    available_pantry: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.dietary_restrictions = {tag.strip().lower() for tag in self.dietary_restrictions}
        self.available_pantry = [item.strip().lower() for item in self.available_pantry]
