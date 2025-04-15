from flask import jsonify, abort

def get_recipes(req):
    # Extract query params
    ingredients = req.args.get("ingredients", "")
    max_time = req.args.get("maxTime")
    cuisine = req.args.get("cuisine")
    meal_type = req.args.get("mealType")

    # TODO: Replace with real filtering logic
    return jsonify([
        {
            "id": "r1",
            "name": "Pasta Primavera",
            "estimatedTime": 30,
            "cuisine": "Italian",
            "mealType": "dinner"
        }
    ])

def get_recipe_by_id(recipe_id):
    # TODO: Fetch recipe from DB
    if recipe_id == "r1":
        return jsonify({
            "id": "r1",
            "name": "Pasta Primavera",
            "ingredients": ["pasta", "vegetables", "olive oil"],
            "steps": ["Boil pasta", "Stir-fry vegetables", "Mix together"],
            "time": 30,
            "cuisine": "Italian",
            "mealType": "dinner"
        })
    else:
        abort(404, "Recipe not found")

def add_recipe(data):
    # TODO: Save to DB
    return jsonify({"id": "r999"}), 201
