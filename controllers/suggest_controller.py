from flask import jsonify

def suggest(filter_data):
    """
    Accepts a JSON with filtering criteria like:
      - ingredients: list of strings
      - maxTime: integer
      - cuisine: string
      - mealType: string
    And returns a list of suggested recipes (mock data for now).
    """
    # Extract parameters from the filter data, with defaults if needed.
    ingredients = filter_data.get("ingredients", [])
    max_time = filter_data.get("maxTime")
    cuisine = filter_data.get("cuisine")
    meal_type = filter_data.get("mealType")

    # TODO: Implement your matching and scoring logic based on the provided filters.
    # For this base implementation, we return a static list of mocked suggestions.
    suggested_recipes = [
        {
            "id": "r1",
            "name": "Pasta Primavera",
            "matchScore": 90.5,
            "estimatedTime": 30,
            "missingIngredients": []  # In a real app, calculate what's missing from the filter.
        },
        {
            "id": "r2",
            "name": "Chicken Tikka Masala",
            "matchScore": 85.0,
            "estimatedTime": 45,
            "missingIngredients": ["yogurt"]
        }
    ]
    return jsonify(suggested_recipes)
