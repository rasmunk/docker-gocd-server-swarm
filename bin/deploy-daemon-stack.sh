#!/bin/bash
# Bail out on errors
set -e

DOCKER=$1
COMPOSE_FILE=$2
SERVICE_NAME=$3

# https://serverfault.com/questions/1115847/docker-stack-deploy-doesnt-resolve-environment-variables-with-default-value-lik
export $(grep -v '^#' .env | xargs)
envsubst < ${COMPOSE_FILE} | ${DOCKER} stack deploy --detach -c - ${SERVICE_NAME}