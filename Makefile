SHELL := /bin/bash
OWNER=ucphhpc
IMAGE=gocd-server-swarm
SERVICE_NAME=gocd
# Enable that the builder should use buildkit
# https://docs.docker.com/develop/develop-images/build_enhancements/
DOCKER_BUILDKIT=1

.PHONY: all init build clean daemon dockerclean down push test

all: init build test

# Link to the original defaults.env if none other is setup
init:
ifeq (,$(wildcard ./.env))
	ln -s defaults.env .env
endif

build:
	docker-compose build ${ARGS}

clean:
	docker rmi -f $(OWNER)/$(IMAGE):$(TAG) $(ARGS)

daemon:
	docker stack deploy -c <(docker-compose config) $(SERVICE_NAME) $(ARGS)

dockerclean:
	docker image prune -f
	docker container prune -f
	docker volume prune -f

down:
	docker stack rm $(SERVICE_NAME) $(ARGS)

push:
	docker push ${OWNER}/${IMAGE}:${TAG} $(ARGS)

test:
# TODO, implement tests