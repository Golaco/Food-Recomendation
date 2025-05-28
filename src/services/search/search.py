from flask import Flask, request, jsonify
from google.cloud import bigquery
import ast, re

app = Flask(__name__)

def clean_recipe(recipe):
    for field in ["NER", "directions", "ingredients"]:
        val = recipe.get(field)
        if val and isinstance(val, str):
            try:
                recipe[field] = ast.literal_eval(val)
            except Exception:
                pass
    return recipe



def fetch_recipes_with_exact_ingredients(ingredients, ingredients_field="ingredients"):
    client = bigquery.Client()
    query = f"""
    SELECT title, ingredients, directions, link, source, NER, site
    FROM `fculcn.raw_recipes.half_recipes`
    WHERE TRUE
    """
    for ingredient in ingredients:
        query += f" AND {ingredients_field} LIKE '%{ingredient}%' "

    query_job = client.query(query)
    results = query_job.result()
    recipes = [clean_recipe(dict(row.items())) for row in results]

    exact_match_recipes = []
    for recipe in recipes:
        recipe_ingredients_list = recipe.get(ingredients_field, [])
        if not isinstance(recipe_ingredients_list, list):
            # if still a string or other, try to parse it
            try:
                recipe_ingredients_list = ast.literal_eval(recipe_ingredients_list)
            except Exception:
                # fallback: split by commas
                recipe_ingredients_list = re.split(r',\s*', str(recipe_ingredients_list))

        # normalize to lowercase strings for matching
        recipe_ingredients_lower = [ri.lower() for ri in recipe_ingredients_list]

        contains_only_given = all(
            any(ingredient.lower() in recipe_ingredient for ingredient in ingredients)
            for recipe_ingredient in recipe_ingredients_lower
        )

        all_given_present = all(
            any(ingredient.lower() in recipe_ingredient for recipe_ingredient in recipe_ingredients_lower)
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
    app.run(host="0.0.0.0", port=5000)
