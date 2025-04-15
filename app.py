from flask import Flask, request, jsonify
from controllers import app_controller, recipes_controller #, metadata_controller, suggest_controller

app = Flask(__name__)

# -------------------- Main Page --------------------
@app.route("/", methods=["GET"])
def get_home():
    return app_controller.get_home(request)


# -------------------- Recipes --------------------
@app.route("/recipes", methods=["GET"])
def get_recipes():
    return recipes_controller.get_recipes(request)

@app.route("/recipes/<recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    return recipes_controller.get_recipe_by_id(recipe_id)

@app.route("/recipes", methods=["POST"])
def add_recipe():
    return recipes_controller.add_recipe(request.json)

# -------------------- Metadata --------------------
@app.route("/cuisines", methods=["GET"])
def get_cuisines():
    return metadata_controller.get_cuisines()

@app.route("/meal-types", methods=["GET"])
def get_meal_types():
    return metadata_controller.get_meal_types()

@app.route("/ingredients", methods=["GET"])
def get_ingredients():
    return metadata_controller.get_ingredients()

# -------------------- Smart Suggestions --------------------
@app.route("/suggest", methods=["POST"])
def suggest():
    return suggest_controller.suggest(request.json)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)

