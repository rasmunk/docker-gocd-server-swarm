#!/bin/bash
DEFAULT_TAG=$1
COMMIT_TAG=$2

if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

# Special tag
make build TAG=${DEFAULT_TAG}
make push TAG=${DEFAULT_TAG}

# Default tag
make build TAG=${COMMIT_TAG}
make push TAG=${COMMIT_TAG}