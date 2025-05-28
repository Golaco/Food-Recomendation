#!/bin/bash

set -e
# Stop on failure

echo "Deleting Kubernetes resources..."

kubectl delete -f services/main/balancer.yaml || true
kubectl delete -f services/main/hpa.yaml || true
kubectl delete -f services/main/deployment.yaml || true

kubectl delete -f services/recommend/hpa.yaml || true
kubectl delete -f services/recommend/deployment.yaml || true

kubectl delete -f services/search/hpa.yaml || true
kubectl delete -f services/search/deployment.yaml || true

echo "Cleanup complete."
