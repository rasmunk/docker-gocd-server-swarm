FROM gocd/gocd-server:v21.3.0

LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

# Default User and Group
ENV USER=go
ENV GROUP=go

ARG UID
ARG GID

# Integrated plugin settings
ARG PLUGIN_SWARM_MAJOR_VERSION
ARG PLUGIN_SWARM_MINOR_VERSION
ARG PLUGIN_SWARM_VERSION
ARG SWARM_JAR_NAME

ARG PLUGIN_GITHUB_MAJOR_VERSION
ARG PLUGIN_GITHUB_MINOR_VERSION
ARG PLUGIN_GITHUB_VERSION
ARG GITHUB_JAR_NAME

ARG GO_DATA_DIR

# Default secret file db
ARG GO_SECRET_DIR
ARG GO_SECRET_FILE

USER root

# Ensure that the timezone is automatically picked up
RUN apk add tzdata

# Add the USER and GROUP
RUN addgroup -g ${GID} ${GROUP} && \
    adduser ${USER} ${GROUP}
g
# Create the secrets file and set permissions
RUN mkdir -p ${GO_SECRET_DIR} && \
    touch ${GO_SECRET_FILE} && \
    chown -R ${USER}:${GROUP} ${GO_SECRET_DIR} && \
    chmod -R 740 ${GO_SECRET_DIR}

USER ${USER}

# Install the docker swarm plugin
RUN wget "https://github.com/gocd-contrib/docker-swarm-elastic-agent-plugin/releases/download/v${PLUGIN_SWARM_VERSION}/${SWARM_JAR_NAME}" -P /tmp/

# Install the GitHub auth plugin
RUN wget "https://github.com/gocd-contrib/github-oauth-authorization-plugin/releases/download/v${PLUGIN_GITHUB_VERSION}/${GITHUB_JAR_NAME}" -P /tmp/

# Create the required diectories
RUN mkdir -p ${GO_DATA_DIR}/plugins/external
# Move the jars into the plugin directory
RUN mv /tmp/${SWARM_JAR_NAME} ${GO_DATA_DIR}/plugins/external/
RUN mv /tmp/${GITHUB_JAR_NAME} ${GO_DATA_DIR}/plugins/external/
