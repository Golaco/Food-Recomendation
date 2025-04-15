from flask import jsonify

# Hardcoded example data; in a real app these may come from a database or configuration file.
CUISINES = ["Italian", "Indian", "Chinese", "Mexican", "French"]
MEAL_TYPES = ["breakfast", "lunch", "dinner", "dessert", "snack"]
INGREDIENTS = ["tomato", "basil", "chicken", "rice", "pasta", "cheese"]

def get_cuisines():
    """
    Return a list of supported cuisines.
    """
    return jsonify(CUISINES)

def get_meal_types():
    """
    Return a list of supported meal types.
    """
    return jsonify(MEAL_TYPES)

def get_ingredients():
    """
    Return a list of available ingredients.
    """
    return jsonify(INGREDIENTS)
