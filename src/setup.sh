#!/bin/bash

set -e  # Exit on error

echo "Building and pushing Docker images..."

# Configuration
PROJECT_ID="fculcn"
REGION="europe"
REPOSITORY_PREFIX="$REGION-docker.pkg.dev/$PROJECT_ID"

# Build and push search service
cd ./services/search
IMAGE="$REPOSITORY_PREFIX/search-service/search-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

# Build and push recommend service
cd ../recommend
IMAGE="$REPOSITORY_PREFIX/recommend-service/recommend-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

# Build and push gateway service
cd ../main
IMAGE="$REPOSITORY_PREFIX/gateway-service/gateway-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

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
