from locust import HttpUser, task, between

class GatewayUser(HttpUser):
    wait_time = between(1, 2)  # Simulates user "think time"

    @task(2)  # Weighted heavier
    def search(self):
        payload = {
            "NER": ["water"]
        }
        self.client.post("/search", json=payload)

    @task(1)
    def recommend(self):
        payload = {
            "NER": ["oil", "sugar", "baking soda", "cinnamon", "eggs", "flour", "salt"],
            "directions": [
                "Mix all together.",
                "Bake at 350° for 35 to 45 minutes in a 9 x 13-inch pan."
            ],
            "ingredients": [
                "2 c. flour",
                "2 c. sugar",
                "1 tsp. salt",
                "2 tsp. cinnamon",
                "2 tsp. baking soda",
                "1 c. oil",
                "4 eggs, added 1 at a time"
            ],
            "link": "www.cookbooks.com/Recipe-Details.aspx?id=810323",
            "site": "www.cookbooks.com",
            "source": "Gathered",
            "title": "Carrot Cake"
        }
        self.client.post("/recommend", json=payload)
