#!/usr/bin/env bash
docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD" $DOCKER_REGISTRY
docker build -t $DOCKER_REGISTRY/$IMAGE ./django
docker push $DOCKER_REGISTRY/$IMAGE
