FROM gocd/gocd-server:v21.3.0

LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

# Default User and Group
ENV USER=go

ARG GROUP
ARG GID

# When the ENV file is passed in
# the docker-compose file
# every env is set
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
ARG GO_PLUGINS_EXTERNAL_DIR
ARG GO_PLUGINS_BUNDLED_DIR

# Default secret db directory
ARG GO_SECRET_DIR

# Update PATH to make java available on the path
ENV PATH="${PATH}:/gocd-jre/bin"

USER root

# Ensure that the timezone is automatically picked up
RUN apk add tzdata py-pip

# Add an extra group an assign it to the ${USER}
RUN addgroup -g ${GID} ${GROUP} && \
    adduser ${USER} ${GROUP} && \
    adduser ${USER} wheel && \
    adduser ${USER} root

# Create the secrets dir and set permissions
RUN mkdir -p ${GO_SECRET_DIR} && \
    chown -R ${USER}:${GROUP} ${GO_SECRET_DIR} && \
    chmod -R 740 ${GO_SECRET_DIR}

USER ${USER}

# Install the docker swarm plugin
RUN wget "https://github.com/gocd-contrib/docker-swarm-elastic-agent-plugin/releases/download/v${PLUGIN_SWARM_VERSION}/${SWARM_JAR_NAME}" -P /tmp/

# Install the GitHub auth plugin
RUN wget "https://github.com/gocd-contrib/github-oauth-authorization-plugin/releases/download/v${PLUGIN_GITHUB_VERSION}/${GITHUB_JAR_NAME}" -P /tmp/

# Create the required diectories
RUN mkdir -p ${GO_PLUGINS_EXTERNAL_DIR} ${GO_PLUGINS_BUNDLED_DIR}
# Move the jars into the plugin directory
RUN mv /tmp/${SWARM_JAR_NAME} ${GO_PLUGINS_EXTERNAL_DIR}/
RUN mv /tmp/${GITHUB_JAR_NAME} ${GO_PLUGINS_EXTERNAL_DIR}/

# Ensure that the plugins are available in the path
ENV PATH="${PATH}:${GO_PLUGINS_EXTERNAL_DIR}:${GO_PLUGINS_BUNDLED_DIR}"

# TODO, uncomment when released
# RUN pip3 install gocd-tools