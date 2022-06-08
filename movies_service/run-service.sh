#!/bin/bash
declare -r NETWORK="movies-system-network"

docker build --tag movies-service -f Dockerfile.movies .
docker run -d --name service-movies -p 5002:5000 --network ${NETWORK} --rm movies-service
