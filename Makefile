OWNER=ucphhpc
IMAGE=gocd-server-swarm
BUILD_TAG=edge
SERVICE_NAME=gocd
ARGS=

.PHONY: build

all: clean build

daemon:
	docker stack deploy --compose-file docker-compose.yml $(SERVICE_NAME) $(ARGS)

down:
	docker stack rm $(SERVICE_NAME) $(ARGS)

build:
	docker-compose build $(ARGS)

dockerclean:
	docker image prune -f
	docker container prune -f
	docker volume prune -f

clean:
	docker rmi -f $(OWNER)/$(IMAGE):$(BUILD_TAG) $(ARGS)

push:
	docker push ${OWNER}/${IMAGE}:${BUILD_TAG} $(ARGS)
