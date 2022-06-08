#!/bin/bash
declare -r NETWORK="movies-system-network"

docker build --tag users-service -f Dockerfile.users .
docker run -d --name service-users -p 5001:5000 --network ${NETWORK} --rm users-service
