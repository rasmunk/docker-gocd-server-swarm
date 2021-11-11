OWNER=ucphhpc
IMAGE=gocd-server-swarm
TAG=edge
SERVICE_NAME=gocd
ARGS=

.PHONY: build

all: clean build test

daemon:
	docker stack deploy --compose-file docker-compose.yml $(SERVICE_NAME)

down:
	docker stack rm $(SERVICE_NAME)

build:
	docker build -t $(OWNER)/$(IMAGE):$(TAG) $(ARGS) .

clean:
	docker rmi -f $(OWNER)/$(IMAGE):$(TAG) $(ARGS)

push:
	docker push ${OWNER}/${IMAGE}:${TAG} $(ARGS)
