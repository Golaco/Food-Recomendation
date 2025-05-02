import re
from flask import Flask, jsonify, request
from google.cloud import bigquery

app = Flask(__name__)

# --- Utility Functions ---

def get_bigquery_client():
    return bigquery.Client()

def fetch_recipes(ingredients=None, max_time=None, cuisine=None, meal_type=None):
    client = get_bigquery_client()
    base_query = """
        SELECT 
            string_field_0 AS name,
            string_field_1 AS ingredients,
            string_field_2 AS steps,
            string_field_3 AS time,
            string_field_4 AS cuisine,
            string_field_5 AS mealType,
            string_field_6 AS link
        FROM `fculcn.raw_recipes.recipes_data`
        WHERE TRUE
    """

    if ingredients:
        for ing in ingredients:
            base_query += f" AND LOWER(string_field_1) LIKE '%{ing.lower()}%' "

    if cuisine:
        base_query += f" AND LOWER(string_field_4) = '{cuisine.lower()}' "

    if meal_type:
        base_query += f" AND LOWER(string_field_5) = '{meal_type.lower()}' "

    if max_time:
        try:
            max_time = int(max_time)
            base_query += f" AND SAFE_CAST(string_field_3 AS INT64) <= {max_time} "
        except ValueError:
            pass

    query_job = client.query(base_query)
    results = query_job.result()
    return [dict(row.items()) for row in results]


@app.route('/recipes', methods=['GET'])
def get_recipes():
    ingredients = request.args.get('ingredients')
    max_time = request.args.get('maxTime')
    cuisine = request.args.get('cuisine')
    meal_type = request.args.get('mealType')

    ingredients_list = [i.strip() for i in ingredients.split(',')] if ingredients else None
    recipes = fetch_recipes(ingredients=ingredients_list, max_time=max_time, cuisine=cuisine, meal_type=meal_type)
    return jsonify(recipes)


@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    max_time = data.get('maxTime')
    cuisine = data.get('cuisine')
    meal_type = data.get('mealType')

    if not ingredients:
        return jsonify({"error": "Missing required field: ingredients"}), 400

    all_recipes = fetch_recipes(ingredients=ingredients, max_time=max_time, cuisine=cuisine, meal_type=meal_type)

    exact_matches = []
    for recipe in all_recipes:
        raw_ingredients = recipe.get("ingredients", "").lower()
        recipe_ingredients_list = re.split(r',\s*', raw_ingredients)

        contains_only_given = all(
            any(ingredient in ing for ingredient in ingredients)
            for ing in recipe_ingredients_list
        )

        all_given_present = all(
            any(ingredient in ing for ing in recipe_ingredients_list)
            for ingredient in ingredients
        )

        if contains_only_given and all_given_present:
            exact_matches.append(recipe)

    return jsonify(exact_matches)


@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    recipes = fetch_recipes()
    all_ingredients = set()
    for recipe in recipes:
        for ing in re.split(r',\s*', recipe.get('ingredients', '').lower()):
            if ing:
                all_ingredients.add(ing)
    return jsonify(sorted(list(all_ingredients)))


@app.route('/cuisines', methods=['GET'])
def get_cuisines():
    recipes = fetch_recipes()
    cuisines = set()
    for recipe in recipes:
        cuisine = recipe.get('cuisine')
        if cuisine:
            cuisines.add(cuisine.lower())
    return jsonify(sorted(list(cuisines)))


@app.route('/meal-types', methods=['GET'])
def get_meal_types():
    recipes = fetch_recipes()
    meal_types = set()
    for recipe in recipes:
        meal_type = recipe.get('mealType')
        if meal_type:
            meal_types.add(meal_type.lower())
    return jsonify(sorted(list(meal_types)))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
