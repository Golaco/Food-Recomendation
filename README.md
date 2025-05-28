"# Food-Recomendation" 


Group 1:
- António Almeida
- Pedro Cardoso

# How to run:

1. Clone the repository to Google Cloud;
2. Add the desired datasets into a Google cloud bucket;
   - Main Dataset - https://www.kaggle.com/datasets/wilmerarltstrmberg/recipe-dataset-over-2m  - This one should be limited to 1m lines
3. Create Google Cloud BigQuery dataset.
3. Open the terminal and navigate to the project directory and into /src:
4. Get the credentials for Google Kubernetes Engine:
```bash
gcloud container clusters get-credentials CLUSTER_NAME--region REGION
```
5. Create secret (must have bigquery access):
```bash
kubectl create secret generic gcp-sa-key --from-file=creds.json=<path-to-your-credentials-file>
```
6. If its the first time running the project, give run permission to both scripts:
```bash
chmod +x setup.sh
chmod +x redeploy.sh
```
7. Run the setup script to deploy the application:
```bash
./setup.sh
```
   - This will create the necessary Kubernetes resources and deploy the application.
7.5 If you want to redeploy the application after a change, run:
```bash
./redeploy.sh
```
   - This will update the existing deployment with the new changes.
8. Get external IP address of the service:
```bash
kubectl get services
```
----------------------------------------------------------------------------------------------------------------------------------
Usage:
9. Access the application using the external IP address and the port 80.
   - Example: `http://<external-ip>/search` or `http://<external-ip>/recommend`

There are currently 2 endpoints available:
- `/search` - A Post endpoint that accepts a JSON body with the following structure:
```json
{
    "ingredients": ["flour", "soda", "cinnamon", "salt", "eggs", "oil", "sugar"]
}
```
- `/recommend` - A Post endpoint that gives recommendations based on the ingredients provided in the request body, exemple:
```json
    {
        "NER": [
            "oil",
            "sugar",
            "baking soda",
            "cinnamon",
            "eggs",
            "flour",
            "salt"
        ],
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
```
You can also just go to `http://<external-ip>/` to check the status of the application.
