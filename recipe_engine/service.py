from typing import List, Dict, Any, Optional
from recipe_engine.models import Recipe, Ingredient, UserPreferences

DEFAULT_RECIPES: List[Recipe] = [
    Recipe(
        id="1",
        title="Avocado Toast with Poached Egg",
        prep_time_minutes=10,
        ingredients=[
            Ingredient(name="bread", amount=2, unit="slices"),
            Ingredient(name="avocado", amount=1, unit="pc"),
            Ingredient(name="egg", amount=2, unit="pcs"),
            Ingredient(name="salt", amount=1, unit="pinch"),
            Ingredient(name="black pepper", amount=1, unit="pinch"),
        ],
        instructions=[
            "Toast the bread slices.",
            "Mash the avocado with salt and black pepper.",
            "Poach the eggs in simmering water for 3 minutes.",
            "Spread mashed avocado over toast and top with poached eggs."
        ],
        dietary_tags={"vegetarian", "dairy-free"},
        calories=350,
        protein_grams=14.0,
        carbs_grams=30.0,
        fat_grams=20.0,
    ),
    Recipe(
        id="2",
        title="Mediterranean Chickpea Salad",
        prep_time_minutes=15,
        ingredients=[
            Ingredient(name="chickpeas", amount=1, unit="can"),
            Ingredient(name="cucumber", amount=1, unit="pc"),
            Ingredient(name="cherry tomatoes", amount=1, unit="cup"),
            Ingredient(name="olive oil", amount=2, unit="tbsp"),
            Ingredient(name="lemon juice", amount=1, unit="tbsp"),
            Ingredient(name="feta cheese", amount=50, unit="grams"),
        ],
        instructions=[
            "Rinse and drain chickpeas.",
            "Dice cucumber and cut cherry tomatoes in half.",
            "Toss chickpeas, cucumber, and tomatoes in a bowl.",
            "Dress with olive oil and lemon juice, crumble feta cheese on top."
        ],
        dietary_tags={"vegetarian", "gluten-free"},
        calories=410,
        protein_grams=15.0,
        carbs_grams=45.0,
        fat_grams=19.0,
    ),
    Recipe(
        id="3",
        title="Grilled Chicken & Broccoli",
        prep_time_minutes=25,
        ingredients=[
            Ingredient(name="chicken breast", amount=200, unit="grams"),
            Ingredient(name="broccoli", amount=150, unit="grams"),
            Ingredient(name="olive oil", amount=1, unit="tbsp"),
            Ingredient(name="garlic", amount=2, unit="cloves"),
            Ingredient(name="salt", amount=1, unit="pinch"),
        ],
        instructions=[
            "Season chicken breast with salt and minced garlic.",
            "Grill chicken for 6-8 minutes per side until cooked through.",
            "Steam broccoli florets until tender-crisp.",
            "Serve hot chicken with steamed broccoli."
        ],
        dietary_tags={"gluten-free", "dairy-free", "keto", "high-protein"},
        calories=380,
        protein_grams=42.0,
        carbs_grams=8.0,
        fat_grams=18.0,
    ),
    Recipe(
        id="4",
        title="Vegan Tofu Stir-Fry",
        prep_time_minutes=20,
        ingredients=[
            Ingredient(name="tofu", amount=200, unit="grams"),
            Ingredient(name="bell pepper", amount=1, unit="pc"),
            Ingredient(name="broccoli", amount=100, unit="grams"),
            Ingredient(name="soy sauce", amount=2, unit="tbsp"),
            Ingredient(name="sesame oil", amount=1, unit="tbsp"),
        ],
        instructions=[
            "Cube tofu and sauté in sesame oil until golden.",
            "Add sliced bell pepper and broccoli florets.",
            "Stir in soy sauce and cook for 5 minutes."
        ],
        dietary_tags={"vegan", "vegetarian", "dairy-free"},
        calories=320,
        protein_grams=20.0,
        carbs_grams=16.0,
        fat_grams=18.0,
    ),
    Recipe(
        id="5",
        title="Classic Garlic Butter Pasta",
        prep_time_minutes=15,
        ingredients=[
            Ingredient(name="pasta", amount=200, unit="grams"),
            Ingredient(name="butter", amount=30, unit="grams"),
            Ingredient(name="garlic", amount=3, unit="cloves"),
            Ingredient(name="parmesan cheese", amount=30, unit="grams"),
            Ingredient(name="parsley", amount=1, unit="tbsp"),
        ],
        instructions=[
            "Boil pasta in salted water until al dente.",
            "Melt butter in a pan and sauté minced garlic.",
            "Toss cooked pasta in garlic butter.",
            "Garnish with grated parmesan cheese and fresh parsley."
        ],
        dietary_tags={"vegetarian"},
        calories=520,
        protein_grams=14.0,
        carbs_grams=68.0,
        fat_grams=22.0,
    ),
]

class RecipeService:
    def __init__(self, recipes: Optional[List[Recipe]] = None):
        self.recipes: List[Recipe] = recipes if recipes is not None else list(DEFAULT_RECIPES)

    def add_recipe(self, recipe: Recipe) -> None:
        """Add a new recipe to the collection."""
        if any(r.id == recipe.id for r in self.recipes):
            raise ValueError(f"Recipe with ID '{recipe.id}' already exists.")
        self.recipes.append(recipe)

    def get_recipe_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """Fetch recipe by its unique ID."""
        for recipe in self.recipes:
            if recipe.id == recipe_id:
                return recipe
        return None

    def calculate_pantry_match(self, recipe: Recipe, pantry: List[str]) -> float:
        """
        Calculate the percentage of recipe ingredients present in pantry.
        Pantry items match if the ingredient name contains or matches the pantry item string.
        """
        if not recipe.ingredients:
            return 100.0

        pantry_set = {item.strip().lower() for item in pantry}
        if not pantry_set:
            return 0.0

        matched_count = 0
        for ing in recipe.ingredients:
            ing_name = ing.name.lower()
            # Match if exact match or if pantry item is contained in ingredient name or vice versa
            if any(p_item in ing_name or ing_name in p_item for p_item in pantry_set):
                matched_count += 1

        return round((matched_count / len(recipe.ingredients)) * 100.0, 2)

    def filter_recipes(
        self,
        preferences: UserPreferences
    ) -> List[Recipe]:
        """
        Filter recipes matching mandatory dietary restrictions and max prep time limit.
        """
        filtered = []
        for recipe in self.recipes:
            # Check dietary restrictions: recipe must contain all requested restriction tags
            if preferences.dietary_restrictions:
                if not preferences.dietary_restrictions.issubset(recipe.dietary_tags):
                    continue

            # Check prep time limit
            if preferences.max_prep_time_minutes is not None:
                if recipe.prep_time_minutes > preferences.max_prep_time_minutes:
                    continue

            filtered.append(recipe)

        return filtered

    def generate_recommendations(
        self,
        preferences: UserPreferences,
        min_pantry_match_pct: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Generate ranked meal recommendations based on user preferences and pantry availability.
        Returns a list of dicts with recipe info and match percentage.
        """
        candidate_recipes = self.filter_recipes(preferences)
        results = []

        for recipe in candidate_recipes:
            match_pct = self.calculate_pantry_match(recipe, preferences.available_pantry)
            if match_pct >= min_pantry_match_pct:
                results.append({
                    "recipe": recipe,
                    "match_percentage": match_pct,
                    "missing_ingredients": self._get_missing_ingredients(recipe, preferences.available_pantry)
                })

        # Sort by match percentage descending, then by prep time ascending
        results.sort(key=lambda x: (-x["match_percentage"], x["recipe"].prep_time_minutes))
        return results

    def _get_missing_ingredients(self, recipe: Recipe, pantry: List[str]) -> List[Ingredient]:
        """Helper to find which recipe ingredients are missing in pantry."""
        pantry_set = {item.strip().lower() for item in pantry}
        missing = []
        for ing in recipe.ingredients:
            ing_name = ing.name.lower()
            if not any(p_item in ing_name or ing_name in p_item for p_item in pantry_set):
                missing.append(ing)
        return missing

    def calculate_nutrition_summary(self, recipes: List[Recipe]) -> Dict[str, float]:
        """Calculate total calories, protein, carbs, and fat across a list of recipes."""
        total_calories = 0.0
        total_protein = 0.0
        total_carbs = 0.0
        total_fat = 0.0

        for r in recipes:
            total_calories += r.calories or 0.0
            total_protein += r.protein_grams or 0.0
            total_carbs += r.carbs_grams or 0.0
            total_fat += r.fat_grams or 0.0

        return {
            "total_calories": round(total_calories, 1),
            "total_protein_g": round(total_protein, 1),
            "total_carbs_g": round(total_carbs, 1),
            "total_fat_g": round(total_fat, 1),
        }
