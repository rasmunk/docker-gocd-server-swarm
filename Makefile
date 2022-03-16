SHELL := /bin/bash
OWNER=ucphhpc
IMAGE=gocd-server-swarm
TAG=edge
SERVICE_NAME=gocd
ARGS=

.PHONY: build

all: clean init build

# Link to the original defaults.env if none other is setup
init:
ifeq (,$(wildcard ./.env))
	ln -s defaults.env .env
endif

daemon:
	docker stack deploy -c <(docker-compose config) $(SERVICE_NAME) $(ARGS)

down:
	docker stack rm $(SERVICE_NAME) $(ARGS)

build:
	docker-compose build --build-arg TAG=$(TAG) $(ARGS)

dockerclean:
	docker image prune -f
	docker container prune -f
	docker volume prune -f

clean:
	docker rmi -f $(OWNER)/$(IMAGE):$(TAG) $(ARGS)

push:
	docker push ${OWNER}/${IMAGE}:${TAG} $(ARGS)

test:
# TODO, implement tests :)
