#!/bin/bash

# Check if IP was provided
if [ -z "$1" ]; then
  echo "Usage: ./test.sh <GATEWAY_URL_OR_IP>"
  exit 1
fi

TARGET="http://$1"

# Run locust with the target host
locust -f locustfile.py --host=$TARGET
