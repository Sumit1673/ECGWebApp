#!/usr/bin/env bash

set -euo pipefail

# echo "Building App"
# docker build -f app/Dockerfile app/

echo "Building Backend"
docker build  -t backend:v1 -f backend/Dockerfile backend/

echo "Running Backend"
docker run --rm -p 8081:8081 backend:v1

echo "Testing the application"
curl --header "Content-Type: application/json" \
        --request POST \
        --data '{"username":"xyz","password":"xyz"}' \
        http://localhost:8081/predict
