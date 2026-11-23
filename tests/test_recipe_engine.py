import pytest
from recipe_engine.models import Ingredient, Recipe, UserPreferences
from recipe_engine.service import RecipeService, DEFAULT_RECIPES

def test_ingredient_validation():
    ing = Ingredient(name="  Tomato  ", amount=2.5, unit="pcs")
    assert ing.name == "tomato"
    assert ing.amount == 2.5
    assert ing.unit == "pcs"

    with pytest.raises(ValueError):
        Ingredient(name="Bad", amount=-1.0, unit="kg")

def test_recipe_validation():
    recipe = Recipe(
        id="test-1",
        title="  Test Recipe  ",
        prep_time_minutes=15,
        ingredients=[Ingredient(name="flour", amount=1, unit="cup")],
        instructions=["Mix flour."],
        dietary_tags={"  Vegan  ", "GLUTEN-FREE"}
    )
    assert recipe.title == "Test Recipe"
    assert recipe.prep_time_minutes == 15
    assert recipe.dietary_tags == {"vegan", "gluten-free"}

    with pytest.raises(ValueError):
        Recipe(
            id="test-2",
            title="Bad Time",
            prep_time_minutes=-5,
            ingredients=[],
            instructions=[]
        )

def test_user_preferences_normalization():
    prefs = UserPreferences(
        dietary_restrictions={"VEGETARIAN", " dairy-free "},
        available_pantry=["  Avocado  ", "EGG"]
    )
    assert prefs.dietary_restrictions == {"vegetarian", "dairy-free"}
    assert prefs.available_pantry == ["avocado", "egg"]

def test_service_initialization():
    service = RecipeService()
    assert len(service.recipes) == len(DEFAULT_RECIPES)

    custom_recipe = Recipe(
        id="custom-1",
        title="Omelette",
        prep_time_minutes=5,
        ingredients=[Ingredient(name="egg", amount=3, unit="pcs")],
        instructions=["Whisk and fry."]
    )
    service.add_recipe(custom_recipe)
    assert service.get_recipe_by_id("custom-1") == custom_recipe

    with pytest.raises(ValueError):
        service.add_recipe(custom_recipe)

def test_pantry_match_calculation():
    service = RecipeService()
    recipe = Recipe(
        id="r-match",
        title="Pancake",
        prep_time_minutes=10,
        ingredients=[
            Ingredient(name="flour", amount=1, unit="cup"),
            Ingredient(name="milk", amount=1, unit="cup"),
            Ingredient(name="egg", amount=1, unit="pc"),
        ],
        instructions=[]
    )

    # 1 out of 3 match
    match_1 = service.calculate_pantry_match(recipe, ["milk"])
    assert match_1 == 33.33

    # 3 out of 3 match
    match_2 = service.calculate_pantry_match(recipe, ["flour", "milk", "egg"])
    assert match_2 == 100.0

    # 0 match
    match_3 = service.calculate_pantry_match(recipe, ["chicken"])
    assert match_3 == 0.0

    # Empty ingredients
    empty_recipe = Recipe(id="empty", title="Air", prep_time_minutes=0, ingredients=[], instructions=[])
    assert service.calculate_pantry_match(empty_recipe, ["milk"]) == 100.0

def test_filter_recipes():
    service = RecipeService()
    
    # Filter by vegetarian and max prep time 15 mins
    prefs = UserPreferences(
        dietary_restrictions={"vegetarian"},
        max_prep_time_minutes=15
    )
    filtered = service.filter_recipes(prefs)
    
    # Should include Avocado Toast (10m, vegetarian) and Mediterranean Chickpea Salad (15m, vegetarian) and Classic Garlic Butter Pasta (15m, vegetarian)
    # Should exclude Grilled Chicken (high protein / non-veg) and Vegan Tofu (20m prep time)
    titles = {r.title for r in filtered}
    assert "Avocado Toast with Poached Egg" in titles
    assert "Mediterranean Chickpea Salad" in titles
    assert "Classic Garlic Butter Pasta" in titles
    assert "Vegan Tofu Stir-Fry" not in titles  # prep time 20 > 15
    assert "Grilled Chicken & Broccoli" not in titles  # not vegetarian

def test_generate_recommendations():
    service = RecipeService()
    prefs = UserPreferences(
        dietary_restrictions={"vegan"},
        available_pantry=["tofu", "bell pepper", "broccoli", "soy sauce", "sesame oil"]
    )
    recs = service.generate_recommendations(prefs, min_pantry_match_pct=50.0)
    assert len(recs) == 1
    assert recs[0]["recipe"].title == "Vegan Tofu Stir-Fry"
    assert recs[0]["match_percentage"] == 100.0
    assert len(recs[0]["missing_ingredients"]) == 0

def test_nutrition_summary():
    service = RecipeService()
    r1 = Recipe(
        id="n1", title="Dish 1", prep_time_minutes=5, ingredients=[], instructions=[],
        calories=200, protein_grams=10.0, carbs_grams=20.0, fat_grams=5.0
    )
    r2 = Recipe(
        id="n2", title="Dish 2", prep_time_minutes=5, ingredients=[], instructions=[],
        calories=300, protein_grams=15.0, carbs_grams=30.0, fat_grams=10.0
    )
    summary = service.calculate_nutrition_summary([r1, r2])
    assert summary["total_calories"] == 500.0
    assert summary["total_protein_g"] == 25.0
    assert summary["total_carbs_g"] == 50.0
    assert summary["total_fat_g"] == 15.0
