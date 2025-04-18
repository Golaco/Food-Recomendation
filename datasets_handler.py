import pandas as pd
import os

# Load the dataset once when the module is imported
DATA_PATH = os.path.join("Dataset", "recipes_data.csv")
recipes_df = pd.read_csv(DATA_PATH)

# Clean and preprocess NER ingredients into sets for easy filtering
recipes_df["ner_clean"] = recipes_df["NER"].apply(
    lambda x: set(i.strip().lower() for i in eval(x)) if isinstance(x, str) else set()
)

def get_filtered_recipes(ingredients=None, max_time=None, cuisine=None, meal_type=None, number_of_recipes=10):
    """
    Iterates over recipes and stops as soon as the specified number of recipes that match the filters is found.
    
    Filters the recipes based on available ingredients (NER-style).
    Other filters (cuisine, mealType) are placeholders and currently are not used.
    """
    results = []
    
    # Pre-calculate the set from input ingredients for efficiency
    if ingredients:
        user_ingredients = set(i.strip().lower() for i in ingredients.split(","))
    else:
        user_ingredients = None

    # Iterate over each row in the dataset until we collect the desired number of recipes
    for _, row in recipes_df.iterrows():
        # If ingredients are provided, check if the recipe's NER ingredients are a subset of user ingredients
        if user_ingredients:
            if not user_ingredients.issuperset(row["ner_clean"]):
                continue

        # Here you could add additional checks for max_time, cuisine, and meal_type if needed
        
        # If the recipe passed the filters, add its summary to the results
        results.append({
            "id": str(row.name),
            "name": row["title"],
            "estimatedTime": 30,  # Placeholder — update if dataset has time
            "cuisine": "Unknown",  # Placeholder
            "mealType": "Unknown"  # Placeholder
        })

        # Stop if we have reached the desired number of recipes
        if len(results) >= number_of_recipes:
            break

    return results

def get_recipe_by_id(recipe_id):
    try:
        row = recipes_df.loc[int(recipe_id)]
        return {
            "id": recipe_id,
            "name": row["title"],
            "ingredients": eval(row["ingredients"]),
            "steps": eval(row["directions"]),
            "time": 30,  # Placeholder
            "cuisine": "Unknown",
            "mealType": "Unknown"
        }
    except (KeyError, ValueError):
        return None


def add_recipe(data):
    # Optional: append to CSV or use a real DB
    return {"id": "new_recipe_id"}
