#!/bin/bash

set -e 
# Stop on failure

echo "Building and pushing Docker images..."

cd ./src/services/search
docker build -t gcr.io/fculcn/search-service:latest .
docker push gcr.io/fculcn/search-service:latest

cd ../recommend
docker build -t gcr.io/fculcn/recommend-service:latest .
docker push gcr.io/fculcn/recommend-service:latest

cd ../main
docker build -t gcr.io/fculcn/gateway-service:latest .
docker push gcr.io/fculcn/gateway-service:latest

cd ../..

echo "Applying Kubernetes deployments and HPA configs..."

kubectl apply -f services/search/deployment.yaml
kubectl apply -f services/search/hpa.yaml

kubectl apply -f services/recommend/deployment.yaml
kubectl apply -f services/recommend/hpa.yaml

kubectl apply -f services/main/deployment.yaml
kubectl apply -f services/main/hpa.yaml
kubectl apply -f services/main/balancer.yaml

echo "Setup complete."
