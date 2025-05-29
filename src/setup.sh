#!/bin/bash

set -e  # Exit on error

# Absolute path to where this script lives (Project root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Building and pushing Docker images..."

PROJECT_ID="fculcn"
REGION="europe"
REPOSITORY_PREFIX="$REGION-docker.pkg.dev/$PROJECT_ID"

# Build and push search service
cd "$SCRIPT_DIR/services/search"
IMAGE="$REPOSITORY_PREFIX/search-service/search-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

# Build and push recommend service
cd "$SCRIPT_DIR/services/recommend"
IMAGE="$REPOSITORY_PREFIX/recommend-service/recommend-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

# Build and push gateway service
cd "$SCRIPT_DIR/services/main"
IMAGE="$REPOSITORY_PREFIX/gateway-service/gateway-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

echo "Applying Kubernetes deployments and HPA configs..."

kubectl apply -f "$SCRIPT_DIR/services/search/deployment.yaml"
kubectl apply -f "$SCRIPT_DIR/services/search/hpa.yaml"

kubectl apply -f "$SCRIPT_DIR/services/recommend/deployment.yaml"
kubectl apply -f "$SCRIPT_DIR/services/recommend/hpa.yaml"

kubectl apply -f "$SCRIPT_DIR/services/main/deployment.yaml"
kubectl apply -f "$SCRIPT_DIR/services/main/hpa.yaml"
kubectl apply -f "$SCRIPT_DIR/services/main/balancer.yaml"

echo "Setup complete."
