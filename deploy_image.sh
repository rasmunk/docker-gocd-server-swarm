#!/bin/bash
BUILD_ARGS=$1
TAG=$2

if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

make build TAG=${TAG} ARGS=${BUILD_ARGS}
make push TAG=${TAG} ARGS=${BUILD_ARGS}
