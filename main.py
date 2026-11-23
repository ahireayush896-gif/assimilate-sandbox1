import sys
from typing import List, Set
from recipe_engine.models import UserPreferences, Recipe, Ingredient
from recipe_engine.service import RecipeService

def print_banner():
    print("=" * 60)
    print(" 🍳 WELCOME TO THE RECIPE & MEAL GENERATOR ENGINE 🥗 ")
    print("=" * 60)
    print("Find delicious meals, manage your pantry, & cook what you have!\n")

def prompt_dietary_restrictions() -> Set[str]:
    print("Select your dietary preferences / restrictions (comma-separated):")
    print("Available tags: vegetarian, vegan, gluten-free, dairy-free, keto, high-protein")
    user_input = input("-> Dietary tags (or press Enter for none): ").strip()
    if not user_input:
        return set()
    return {tag.strip().lower() for tag in user_input.split(",")}

def prompt_max_prep_time() -> int:
    while True:
        user_input = input("-> Maximum prep time in minutes (or press Enter for no limit): ").strip()
        if not user_input:
            return None
        try:
            val = int(user_input)
            if val < 0:
                print("Prep time cannot be negative. Try again.")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer number of minutes.")

def prompt_pantry_items() -> List[str]:
    print("\nEnter ingredients currently in your pantry (comma-separated):")
    print("Example: bread, avocado, eggs, chicken breast, garlic, olive oil, salt")
    user_input = input("-> Pantry items (or press Enter for empty pantry): ").strip()
    if not user_input:
        return []
    return [item.strip().lower() for item in user_input.split(",")]

def display_recommendations(recommendations: List[dict]):
    if not recommendations:
        print("\n❌ No recipes found matching your criteria and pantry items.")
        print("Try relaxing your dietary restrictions or increasing max prep time.")
        return

    print(f"\n✨ Found {len(recommendations)} matching recipe(s):")
    print("-" * 60)

    for idx, rec in enumerate(recommendations, 1):
        recipe: Recipe = rec["recipe"]
        match_pct = rec["match_percentage"]
        missing: List[Ingredient] = rec["missing_ingredients"]

        print(f"\n{idx}. {recipe.title.upper()} (ID: {recipe.id})")
        print(f"   ⏱️  Prep Time: {recipe.prep_time_minutes} mins")
        print(f"   🏷️  Dietary Tags: {', '.join(recipe.dietary_tags) if recipe.dietary_tags else 'none'}")
        if recipe.calories:
            print(f"   🔥 Nutrition: {recipe.calories} kcal | Protein: {recipe.protein_grams}g | Carbs: {recipe.carbs_grams}g | Fat: {recipe.fat_grams}g")
        print(f"   🛒 Pantry Match: {match_pct}%")
        
        if missing:
            missing_str = ", ".join([f"{m.amount} {m.unit} {m.name}" for m in missing])
            print(f"   ⚠️  Missing Ingredients: {missing_str}")
        else:
            print("   🎉 You have all ingredients in your pantry!")
        
        print("   📜 Ingredients:")
        for ing in recipe.ingredients:
            print(f"      - {ing.amount} {ing.unit} {ing.name}")

        print("   🍳 Instructions:")
        for step_no, step in enumerate(recipe.instructions, 1):
            print(f"      {step_no}. {step}")
        print("-" * 60)

def handle_add_recipe(service: RecipeService):
    print("\n--- Add New Recipe ---")
    recipe_id = input("Recipe ID (e.g., '6'): ").strip()
    if not recipe_id:
        print("ID cannot be empty.")
        return
    if service.get_recipe_by_id(recipe_id):
        print(f"Recipe with ID '{recipe_id}' already exists.")
        return

    title = input("Recipe Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    try:
        prep_time = int(input("Prep Time (minutes): ").strip())
    except ValueError:
        print("Invalid number for prep time.")
        return

    print("Enter ingredients (format: name,amount,unit). Type 'done' when finished.")
    ingredients = []
    while True:
        line = input("  Ingredient (e.g. tomato,2,pcs or 'done'): ").strip()
        if line.lower() == 'done' or not line:
            break
        parts = line.split(',')
        if len(parts) != 3:
            print("  Invalid format. Use name,amount,unit")
            continue
        try:
            name, amount_str, unit = parts[0].strip(), parts[1].strip(), parts[2].strip()
            amount = float(amount_str)
            ingredients.append(Ingredient(name=name, amount=amount, unit=unit))
        except ValueError:
            print("  Invalid amount number. Try again.")

    if not ingredients:
        print("Recipe must have at least one ingredient.")
        return

    print("Enter instructions step by step. Type 'done' when finished.")
    instructions = []
    step_idx = 1
    while True:
        step = input(f"  Step {step_idx} (or 'done'): ").strip()
        if step.lower() == 'done' or not step:
            break
        instructions.append(step)
        step_idx += 1

    tags_input = input("Dietary tags (comma-separated, e.g. vegan,gluten-free): ").strip()
    tags = {t.strip().lower() for t in tags_input.split(",")} if tags_input else set()

    try:
        calories = float(input("Calories (optional, press Enter to skip): ").strip() or 0) or None
        protein = float(input("Protein in grams (optional, press Enter to skip): ").strip() or 0) or None
        carbs = float(input("Carbs in grams (optional, press Enter to skip): ").strip() or 0) or None
        fat = float(input("Fat in grams (optional, press Enter to skip): ").strip() or 0) or None
    except ValueError:
        calories, protein, carbs, fat = None, None, None, None

    new_recipe = Recipe(
        id=recipe_id,
        title=title,
        prep_time_minutes=prep_time,
        ingredients=ingredients,
        instructions=instructions,
        dietary_tags=tags,
        calories=int(calories) if calories is not None else None,
        protein_grams=protein,
        carbs_grams=carbs,
        fat_grams=fat,
    )

    service.add_recipe(new_recipe)
    print(f"\n✅ Successfully added recipe '{title}' (ID: {recipe_id})!")

def main():
    service = RecipeService()

    if len(sys.argv) > 1 and sys.argv[1] == "--cli-demo":
        # Non-interactive quick demo mode for testing
        print("Running quick demo mode...")
        prefs = UserPreferences(
            dietary_restrictions={"vegetarian"},
            max_prep_time_minutes=20,
            available_pantry=["bread", "avocado", "eggs", "salt", "black pepper", "chickpeas", "cucumber", "pasta", "butter", "garlic"]
        )
        recs = service.generate_recommendations(prefs, min_pantry_match_pct=0.0)
        display_recommendations(recs)
        return

    print_banner()

    while True:
        print("\nMAIN MENU:")
        print("1. Find Recipe Recommendations & Meal Suggestions")
        print("2. Browse All Available Recipes")
        print("3. Add a New Recipe")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            print("\n--- Recipe Recommendation Wizard ---")
            dietary = prompt_dietary_restrictions()
            max_time = prompt_max_prep_time()
            pantry = prompt_pantry_items()

            prefs = UserPreferences(
                dietary_restrictions=dietary,
                max_prep_time_minutes=max_time,
                available_pantry=pantry
            )

            while True:
                try:
                    min_match_str = input("Minimum pantry match percentage required (0-100, default 0): ").strip()
                    min_match = float(min_match_str) if min_match_str else 0.0
                    if 0.0 <= min_match <= 100.0:
                        break
                    print("Please enter a value between 0 and 100.")
                except ValueError:
                    print("Please enter a valid number.")

            recs = service.generate_recommendations(prefs, min_pantry_match_pct=min_match)
            display_recommendations(recs)

            if recs:
                calc_nutr = input("\nWould you like to calculate total nutrition for these recommended recipes? (y/n): ").strip().lower()
                if calc_nutr == 'y':
                    rec_recipes = [r["recipe"] for r in recs]
                    nutr = service.calculate_nutrition_summary(rec_recipes)
                    print("\n📊 Nutrition Summary for Recommended Meals:")
                    print(f"   - Total Calories: {nutr['total_calories']} kcal")
                    print(f"   - Total Protein: {nutr['total_protein_g']}g")
                    print(f"   - Total Carbs: {nutr['total_carbs_g']}g")
                    print(f"   - Total Fat: {nutr['total_fat_g']}g")

        elif choice == '2':
            print("\n--- All Available Recipes ---")
            display_recommendations([
                {
                    "recipe": r,
                    "match_percentage": 100.0,
                    "missing_ingredients": []
                }
                for r in service.recipes
            ])

        elif choice == '3':
            handle_add_recipe(service)

        elif choice == '4':
            print("\nThank you for using the Recipe & Meal Generator Engine. Bon appétit! 🍽️")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
