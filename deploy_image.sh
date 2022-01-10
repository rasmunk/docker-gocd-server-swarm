#!/bin/bash
IMAGE_TAG=$1
DEFAULT_TAG=$2

if [[ -n ${DOCKERHUB_USERNAME} ]] && [[ -n ${DOCKERHUB_PASSWORD} ]]; then
    echo "${DOCKERHUB_PASSWORD}" | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
fi

# Special tag
make build TAG=${IMAGE_TAG}
make push TAG=${IMAGE_TAG}

# Default tag
make build TAG=${DEFAULT_TAG}
make push TAG=${DEFAULT_TAG}
