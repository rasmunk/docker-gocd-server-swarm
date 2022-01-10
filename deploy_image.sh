#!/bin/bash
TAG=$1

if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

make build TAG=${TAG}
make push TAG=${TAG}