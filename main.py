from flask import Flask, request, jsonify
from google.cloud import bigquery
import re

app = Flask(__name__)

def fetch_recipes_with_exact_ingredients(ingredients, ingredients_field="string_field_1"):
    client = bigquery.Client()
    query = f"""
    SELECT string_field_0, string_field_1, string_field_2, string_field_3, string_field_4, string_field_5, string_field_6
    FROM `fculcn.raw_recipes.recipes_data`
    WHERE TRUE
    """
    for ingredient in ingredients:
        query += f" AND {ingredients_field} LIKE '%{ingredient}%' "

    query_job = client.query(query)
    results = query_job.    result()
    recipes = [dict(row.items()) for row in results]

    exact_match_recipes = []
    for recipe in recipes:
        recipe_ingredients = recipe.get(ingredients_field, "").lower()
        if not recipe_ingredients:
            continue

        recipe_ingredients_list = re.split(r',\s*', recipe_ingredients)

        contains_only_given = all(
            any(ingredient.lower() in recipe_ingredient for ingredient in ingredients)
            for recipe_ingredient in recipe_ingredients_list
        )

        all_given_present = all(
            any(ingredient.lower() in recipe_ingredient for recipe_ingredient in recipe_ingredients_list)
            for ingredient in ingredients
        )

        if contains_only_given and all_given_present:
            exact_match_recipes.append(recipe)

    return exact_match_recipes

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    try:
        results = fetch_recipes_with_exact_ingredients(ingredients)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
