"# Food-Recomendation" 


Group 1:
- António Almeida
- Pedro Cardoso

# How to run:

1. Clone the repository to Google Cloud;
2. Add the desired datasets into a Google cloud bucket;
   - Main Dataset - https://www.kaggle.com/datasets/wilmerarltstrmberg/recipe-dataset-over-2m
   - Secondary Dataset - https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions
3. Create Google Cloud BigQuery dataset.
3. Open the terminal and navigate to the project directory;
4. Get the credentials for Google Kubernetes Engine:
```bash
gcloud container clusters get-credentials proj-cluster --region europe-west4
```
5. Create secret (must have bigquery access):
```bash
kubectl create secret generic gcp-sa-key --from-file=creds.json=<path-to-your-credentials-file>
```
6. Build the Docker image:
```bash
docker build -t gcr.io/fculcn/recipe-api:latest .
docker push gcr.io/fculcn/recipe-api:latest
```
7. Deploy the application to Kubernetes:
```bash
kubectl apply -f deployment.yaml
```
8. Get external IP address of the service:
```bash
kubectl get services
```
