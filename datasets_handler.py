# TODO create dataset handler using pandas

import pandas as pd
import os

# Load the dataset once when the module is imported
DATA_PATH = os.path.join("data", "recipes.csv")
recipes_df = pd.read_csv(DATA_PATH)

# Clean and preprocess NER ingredients into sets for easy filtering
recipes_df["ner_clean"] = recipes_df["NER"].apply(
    lambda x: set(i.strip().lower() for i in eval(x)) if isinstance(x, str) else set()
)

def get_filtered_recipes(ingredients=None, max_time=None, cuisine=None, meal_type=None):
    """
    Filters the recipes based on available ingredients (NER-style).
    Other filters (cuisine, mealType) are ignored for now unless the dataset is expanded.
    """
    filtered = recipes_df.copy()

    # Only filter if ingredients are provided
    if ingredients:
        user_ingredients = set(i.strip().lower() for i in ingredients.split(","))
        filtered = filtered[filtered["ner_clean"].apply(lambda ner: user_ingredients.issuperset(ner))]

    # Format result as summaries
    results = []
    for _, row in filtered.iterrows():
        results.append({
            "id": str(row.name),
            "name": row["title"],
            "estimatedTime": 30,  # Placeholder — update if dataset has time
            "cuisine": "Unknown",  # Placeholder
            "mealType": "Unknown"  # Placeholder
        })

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
