from flask import Flask, request, jsonify
import pandas as pd
from google.cloud import bigquery
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import ast, re

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    title = data.get("title", "")
    NER = data.get("NER", [])

    if not title or not NER:
        return jsonify({"error": "Missing title or ingredients"}), 400

    try:
        recommendations = get_recommendations(title, NER, top_k=5, random_sample=True)
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_recommendations(title, ingredients, top_k=5, random_sample=False):
    client = bigquery.Client()
    query = """
            SELECT title, NER, ingredients, directions, link, source, site
            FROM `fculcn.raw_recipes.half_recipes`
            WHERE title IS NOT NULL
            AND NER IS NOT NULL LIMIT 1000
            """
    query_job = client.query(query)
    results = query_job.result()
    df = pd.DataFrame([dict(row) for row in results])

    def parse_ner_field(x):
        if isinstance(x, list):
            return x
        if isinstance(x, str):
            try:
                return ast.literal_eval(x)
            except:
                return []
        return []

    df["NER"] = df["NER"].apply(parse_ner_field)

    df["text"] = df["title"].fillna("") + " " + df["NER"].apply(
        lambda x: " ".join(x) if isinstance(x, list) else "")

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["text"])

    knn = NearestNeighbors(n_neighbors=min(top_k * 2, len(df)), metric='cosine')
    knn.fit(X)

    query_text = title + " " + " ".join(ingredients)
    query_vector = vectorizer.transform([query_text])
    distances, indices = knn.kneighbors(query_vector, n_neighbors=min(top_k * 2, len(df)))

    results = df.iloc[indices[0]].copy()
    if random_sample:
        results = results.sample(n=min(top_k, len(results)))

    output = results.to_dict(orient="records")

    # Clean ingredients if needed
    for r in output:
        ingredients = r.get("ingredients")
        if isinstance(ingredients, str):
            try:
                r["ingredients"] = ast.literal_eval(ingredients)
            except Exception:
                r["ingredients"] = re.split(r',\s*', ingredients)

    for r in output:
        r.pop("source", None)
        r.pop("site", None)


    # Clean ingredients if needed
    for r in output:
        ingredients = r.get("ingredients")
        if isinstance(ingredients, str):
            try:
                r["ingredients"] = ast.literal_eval(ingredients)
            except Exception:
                r["ingredients"] = re.split(r',\s*', ingredients)

    return output

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
