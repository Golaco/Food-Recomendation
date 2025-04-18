from flask import jsonify, request, abort
import datasets_handler as dataset  

def get_recipes(req):
    ingredients = req.args.get("ingredients")
    max_time = req.args.get("maxTime")
    cuisine = req.args.get("cuisine")
    meal_type = req.args.get("mealType")

    results = dataset.get_filtered_recipes(
        ingredients=ingredients,
        max_time=max_time,
        cuisine=cuisine,
        meal_type=meal_type,
        number_of_recipes=5
    )

    return jsonify(results)

def get_recipe_by_id(recipe_id):
    recipe = dataset.get_recipe_by_id(recipe_id)
    if recipe:
        return jsonify(recipe)
    abort(404, "Recipe not found")

def add_recipe(data):
    new_recipe = dataset.add_recipe(data)
    return jsonify(new_recipe), 201
