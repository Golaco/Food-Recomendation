#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN_MODE=${DRY_RUN_MODE:-client}

echo "Building and pushing Docker images..."

PROJECT_ID="fculcn"
REGION="europe"
REPOSITORY_PREFIX="$REGION-docker.pkg.dev/$PROJECT_ID"

cd "$SCRIPT_DIR/services/search"
IMAGE="$REPOSITORY_PREFIX/search-service/search-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

cd "$SCRIPT_DIR/services/recommend"
IMAGE="$REPOSITORY_PREFIX/recommend-service/recommend-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

cd "$SCRIPT_DIR/services/main"
IMAGE="$REPOSITORY_PREFIX/gateway-service/gateway-service:latest"
docker build -t "$IMAGE" .
docker push "$IMAGE"

echo "Applying Kubernetes deployments and HPA configs (dry run mode: $DRY_RUN_MODE)..."

if [[ "$DRY_RUN_MODE" == "client" ]]; then
  DRY_RUN_FLAG="--dry-run=client"
elif [[ "$DRY_RUN_MODE" == "server" ]]; then
  DRY_RUN_FLAG="--dry-run=server"
else
  DRY_RUN_FLAG=""
fi

kubectl apply $DRY_RUN_FLAG -f "$SCRIPT_DIR/services/search/deployment.yaml"
kubectl apply $DRY_RUN_FLAG -f "$SCRIPT_DIR/services/search/hpa.yaml"

kubectl apply $DRY_RUN_FLAG -f "$SCRIPT_DIR/services/recommend/deployment.yaml"
kubectl apply $DRY_RUN_FLAG -f "$SCRIPT_DIR/services/recommend/hpa.yaml"

kubectl apply $DRY_RUN_FLAG -f "$SCRIPT_DIR/services/main/deployment.yaml"
kubectl apply $DRY_RUN_FLAG -f "$SCRIPT_DIR/services/main/hpa.yaml"
kubectl apply $DRY_RUN_FLAG -f "$SCRIPT_DIR/services/main/balancer.yaml"

echo "Setup complete."
