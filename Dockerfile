FROM gocd/gocd-server:v21.3.0

LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

ARG PLUGIN_SWARM_MAJOR_VERSION=5.0.0
ARG PLUGIN_SWARM_MINOR_VERSION=178
ARG PLUGIN_SWARM_VERSION=${PLUGIN_SWARM_MAJOR_VERSION}-${PLUGIN_SWARM_MINOR_VERSION}
ARG SWARM_JAR_NAME=docker-swarm-elastic-agents-${PLUGIN_SWARM_VERSION}.jar

ARG PLUGIN_GITHUB_MAJOR_VERSION=3.0.2
ARG PLUGIN_GITHUB_MINOR_VERSION=57
ARG PLUGIN_GITHUB_VERSION=${PLUGIN_GITHUB_MAJOR_VERSION}-${PLUGIN_GITHUB_MINOR_VERSION}
ARG GITHUB_JAR_NAME=github-oauth-authorization-plugin-${PLUGIN_GITHUB_VERSION}.jar

ARG GO_DATA_DIR=/godata

USER root
# Ensure that the timezone is automatically picked up
RUN apk add tzdata

USER go
# Install the docker swarm plugin
RUN wget "https://github.com/gocd-contrib/docker-swarm-elastic-agent-plugin/releases/download/v${PLUGIN_SWARM_VERSION}/${SWARM_JAR_NAME}" -P /tmp/

# Install the GitHub auth plugin
RUN wget "https://github.com/gocd-contrib/github-oauth-authorization-plugin/releases/download/v${PLUGIN_GITHUB_VERSION}/${GITHUB_JAR_NAME}" -P /tmp/


# Create the required diectories
RUN mkdir -p ${GO_DATA_DIR}/plugins/external
# Move the jars into the plugin directory
RUN mv /tmp/${SWARM_JAR_NAME} ${GO_DATA_DIR}/plugins/external/
RUN mv /tmp/${GITHUB_JAR_NAME} ${GO_DATA_DIR}/plugins/external/