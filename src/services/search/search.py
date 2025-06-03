from flask import Flask, request, jsonify
from google.cloud import bigquery
import time
import re
import json

app = Flask(__name__)

max_Results = 10
results_threshold = 0.5 

# Map diet types to BigQuery table names
TABLE_MAP = {
    "general": "fculcn.raw_recipes.half_recipes",
    "vegetarian": "fculcn.raw_recipes.vegetarian_recipes",
    "vegan": "fculcn.raw_recipes.vegan_recipes",
    "gluten_free": "fculcn.raw_recipes.gluten_free_recipes",
}

# Initialize BigQuery client
bq_client = bigquery.Client()


def normalize_ingredients(ingredients):
    """
    Normalize ingredients: lowercase, strip, remove punctuation, simple singularization.
    Handles various input types, including lists, strings, and non-string elements.
    """

    def simple_singular(word):
        if len(word) > 3:
            if word.endswith("ies"):
                return word[:-3] + "y"
            if word.endswith("s") and not word.endswith("ss"):
                return word[:-1]
        return word

    normalized = set()
    iterable_ingredients = (
        ingredients if isinstance(ingredients, list) else [ingredients]
    )

    for i in iterable_ingredients:
        if not isinstance(i, str):
            continue
        i_clean = i.strip().lower()
        i_clean = re.sub(r'[.,;:!?"\'()]', "", i_clean)
        i_clean = simple_singular(i_clean)
        normalized.add(i_clean)
    return normalized


def fetch_recipes_by_ner(available_ingredients, table_name, max_matches=max_Results):
    input_set = {i.strip().lower() for i in available_ingredients if isinstance(i, str)}
    if not input_set:
        return []

    input_list = list(input_set)
    input_array_literal = "[" + ", ".join([f'"{i}"' for i in input_list]) + "]"

    query = f"""
    SELECT DISTINCT
        r.title,
        r.ingredients,
        r.directions,
        r.link,
        r.source,
        r.site,
        r.NER,
        ARRAY_LENGTH(r.NER) AS ner_len
    FROM `{table_name}` r
    WHERE
        ARRAY_LENGTH(r.NER) > 0
        AND NOT EXISTS (
            SELECT 1
            FROM UNNEST(r.NER) AS ner
            WHERE LOWER(ner) NOT IN UNNEST({input_array_literal})
        )
    ORDER BY ner_len DESC
    LIMIT {max_matches}
    """

    query_job = bq_client.query(query)
    rows = query_job.result()

    results = []
    for row in rows:
        recipe = dict(row.items())
        recipe["NER"] = sorted([i.lower() for i in recipe.get("NER", [])])
        results.append(recipe)

    return results






def make_search_endpoint(diet_type):
    def endpoint():
        start = time.time()
        data = request.get_json()
        ingredients = data.get("NER") if data else None

        if not ingredients:
            return jsonify({"error": "Missing 'NER' parameter in request body"}), 400

        table_name = TABLE_MAP.get(diet_type)
        if not table_name:
            return jsonify({"error": f"Invalid diet type specified: {diet_type}"}), 400

        try:
            results = fetch_recipes_by_ner(ingredients, table_name)
            elapsed = time.time() - start
            return jsonify(
                {
                    "count": len(results),
                    "time_seconds": round(elapsed, 2),
                    "results": results,
                }
            )
        except Exception as e:
            print(f"Error fetching recipes for {diet_type}: {e}")
            return (
                jsonify({"error": f"An internal server error occurred: {str(e)}"}),
                500,
            )

    endpoint.__name__ = f"search_{diet_type}_ner_endpoint"
    return endpoint


# Register endpoints
app.add_url_rule("/search", view_func=make_search_endpoint("general"), methods=["POST"])
app.add_url_rule(
    "/search/vegetarian", view_func=make_search_endpoint("vegetarian"), methods=["POST"]
)
app.add_url_rule(
    "/search/vegan", view_func=make_search_endpoint("vegan"), methods=["POST"]
)
app.add_url_rule(
    "/search/gluten_free",
    view_func=make_search_endpoint("gluten_free"),
    methods=["POST"],
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)