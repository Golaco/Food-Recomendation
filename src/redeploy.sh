#!/bin/bash

set -e
# Stop on failure

echo "Rebuilding and pushing Docker images..."

cd ./services/search
docker build -t gcr.io/fculcn/search-service:latest .
docker push gcr.io/fculcn/search-service:latest

cd ../recommend
docker build -t gcr.io/fculcn/recommend-service:latest .
docker push gcr.io/fculcn/recommend-service:latest

cd ../main
docker build -t gcr.io/fculcn/gateway-service:latest .
docker push gcr.io/fculcn/gateway-service:latest
cd ../..

cd ./recipe-api
docker build -t gcr.io/fculcn/recipe-api:latest .
docker push gcr.io/fculcn/recipe-api:latest
cd ..

echo "Applying updated Kubernetes deployments..."

kubectl apply -f services/search/deployment.yaml
kubectl apply -f services/recommend/deployment.yaml
kubectl apply -f services/main/deployment.yaml
kubectl apply -f recipe-api/deployment.yaml

echo "Restarting all pods..."
kubectl delete pods --all

echo "Redeploy complete."
