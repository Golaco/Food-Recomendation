import os
import pandas as pd
from flask import Flask, jsonify, request
from collections import defaultdict

app = Flask(__name__)
DATASET_FOLDER = 'Dataset'
recipes_data = []

def load_main_dataset_recipes(file_path):
    """Loads recipe data from a CSV file with the 'Main Dataset' structure."""
    try:
        df = pd.read_csv(file_path)
        df.columns = map(str.lower, df.columns)  # Ensure lowercase column names
        if {'title', 'ingredients', 'directions'}.issubset(df.columns):
            print(f"Processing Main Dataset file: {file_path}")
            for index, row in df.iterrows():
                recipe = {
                    'id': hash(row['link']) if 'link' in row else hash(row['title']), # Create a unique ID
                    'name': row['title'],
                    'ingredients': [ing.strip() for ing in str(row['ingredients']).split(',')],
                    'steps': [step.strip() for step in str(row['directions']).split(';')],
                    'time': None,  # Time information is not present in this dataset
                    'cuisine': None, # Cuisine information is not present
                    'mealType': None # Meal type information is not present
                }
                recipes_data.append(recipe)
            print(f"Loaded {len(df)} recipes from {file_path}")
        else:
            print(f"Warning: CSV file {file_path} does not match Main Dataset structure. Skipping.")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")

# Load data from all CSV files in the Dataset folder
if not os.path.exists(DATASET_FOLDER):
    os.makedirs(DATASET_FOLDER)
    print(f"Created '{DATASET_FOLDER}' folder. Please add your CSV files there.")
else:
    for filename in os.listdir(DATASET_FOLDER):
        if filename.endswith(".csv"):
            file_path = os.path.join(DATASET_FOLDER, filename)
            # We are only trying to load files that match the Main Dataset structure for recipes
            # You might need a different logic if you want to use the other datasets for other purposes
            load_main_dataset_recipes(file_path)

# Ensure recipe IDs are unique (if loading from multiple files)
unique_recipes = []
seen_ids = set()
for recipe in recipes_data:
    if recipe['id'] not in seen_ids:
        unique_recipes.append(recipe)
        seen_ids.add(recipe['id'])
recipes_data = unique_recipes

# --- Utility Functions ---

def filter_recipes(recipes, ingredients=None, max_time=None, cuisine=None, meal_type=None):
    """Filters a list of recipes based on criteria."""
    filtered = recipes
    if ingredients:
        ingredient_list = [ing.strip().lower() for ing in ingredients.split(',')]
        filtered = [
            r for r in filtered if all(ing in [r_ing.strip().lower() for r_ing in r['ingredients']] for ing in ingredient_list)
        ]
    if max_time is not None:
        try:
            max_time = int(max_time)
            filtered = [r for r in filtered if r['time'] is not None and r['time'] <= max_time]
        except ValueError:
            pass
    if cuisine:
        filtered = [r for r in filtered if r['cuisine'] is not None and r['cuisine'].lower() == cuisine.lower()]
    if meal_type:
        filtered = [r for r in filtered if r['mealType'] is not None and r['mealType'].lower() == meal_type.lower()]
    return filtered

def get_unique_values(recipes, key):
    """Extracts and returns a set of unique values for a given key in a list of recipes."""
    values = set()
    for recipe in recipes:
        if key in recipe and recipe[key] is not None:
            if isinstance(recipe[key], list):
                for item in recipe[key]:
                    values.add(item.strip().lower())
            else:
                values.add(str(recipe[key]).strip().lower())
    return sorted(list(values))

# --- API Endpoints ---

@app.route('/recipes', methods=['GET'])
def get_recipes():
    """Fetches recipes, optionally filtered."""
    ingredients = request.args.get('ingredients')
    max_time = request.args.get('maxTime')
    cuisine = request.args.get('cuisine')
    meal_type = request.args.get('mealType')
    filtered_recipes = filter_recipes(recipes_data, ingredients, max_time, cuisine, meal_type)
    return jsonify(filtered_recipes)

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    """Retrieves detailed information of a recipe given its ID."""
    recipe = next((r for r in recipes_data if r['id'] == recipe_id), None)
    if recipe:
        return jsonify(recipe)
    return jsonify({'message': 'Recipe not found'}), 404

@app.route('/recipes', methods=['POST'])
def add_new_recipe():
    """Adds a new recipe to the database."""
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'ingredients', 'steps']):
        return jsonify({'message': 'Missing required fields: name, ingredients, steps'}), 400

    new_recipe = {
        'id': max(r['id'] for r in recipes_data) + 1 if recipes_data else 1,
        'name': data['name'],
        'ingredients': [ing.strip() for ing in data['ingredients']],
        'steps': [step.strip() for step in data['steps']],
        'time': data.get('time'),
        'cuisine': data.get('cuisine'),
        'mealType': data.get('mealType')
    }
    recipes_data.append(new_recipe)
    return jsonify(new_recipe), 201

@app.route('/cuisines', methods=['GET'])
def get_cuisines():
    """Fetches the list of available cuisines."""
    cuisines = get_unique_values(recipes_data, 'cuisine')
    return jsonify(cuisines)

@app.route('/meal-types', methods=['GET'])
def get_meal_types():
    """Fetches the list of available meal types."""
    meal_types = get_unique_values(recipes_data, 'mealType')
    return jsonify(meal_types)

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    """Fetches the list of available ingredients."""
    all_ingredients = set()
    for recipe in recipes_data:
        for ingredient in recipe['ingredients']:
            all_ingredients.add(ingredient.strip().lower())
    return jsonify(sorted(list(all_ingredients)))

@app.route('/suggest', methods=['POST'])
def suggest_recipes():
    """Suggests recipes based on smart filters."""
    data = request.get_json()
    if not data or 'ingredients' not in data:
        return jsonify({'message': 'Missing required field: ingredients'}), 400

    available_ingredients = [ing.strip().lower() for ing in data['ingredients']]
    max_time = data.get('maxTime')
    cuisine = data.get('cuisine')
    meal_type = data.get('mealType')

    suggestions = []
    for recipe in recipes_data:
        recipe_ingredients_lower = [ing.strip().lower() for ing in recipe['ingredients']]
        if all(available_ing in recipe_ingredients_lower for available_ing in available_ingredients):
            # Check optional filters
            if max_time is not None and recipe['time'] is not None and recipe['time'] > int(max_time):
                continue
            if cuisine and recipe['cuisine'] is not None and recipe['cuisine'].lower() != cuisine.lower():
                continue
            if meal_type and recipe['mealType'] is not None and recipe['mealType'].lower() != meal_type.lower():
                continue
            suggestions.append(recipe)

    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True, port=3000)