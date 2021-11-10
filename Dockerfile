FROM gocd/gocd-server:v21.3.0

LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

ARG PLUGIN_SWARM_MAJOR_VERSION=5.0.0
ARG PLUGIN_SWARM_MINOR_VERSION=178
ARG PLUGIN_SWARM_VERSION=${PLUGIN_SWARM_MAJOR_VERSION}-${PLUGIN_SWARM_MINOR_VERSION}
ARG JAR_NAME=docker-swarm-elastic-agents-${PLUGIN_SWARM_VERSION}.jar

ARG GO_DATA_DIR=/godata

USER root
# Ensure that the timezone is automatically picked up
RUN apk add tzdata

USER go
# Install the docker swarm plugin
RUN wget "https://github.com/gocd-contrib/docker-swarm-elastic-agent-plugin/releases/download/v${PLUGIN_SWARM_VERSION}/${JAR_NAME}" -P /tmp/

# Create the required diectories
RUN mkdir -p ${GO_DATA_DIR}/plugins/external
# Move the jar into the plugin directory
RUN mv /tmp/${JAR_NAME} ${GO_DATA_DIR}/plugins/external/
