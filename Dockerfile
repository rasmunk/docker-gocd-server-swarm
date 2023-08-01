FROM gocd/gocd-server:v23.2.0

LABEL MAINTAINER="Rasmus Munk <rasmus.munk@nbi.ku.dk>"

# Default User and Group
ENV USER=go

ARG GROUP
ARG GID

# When the ENV file is passed in
# the docker-compose file
# every env is set
# Integrated plugin settings

# Docker Swarm Plugin
ARG PLUGIN_SWARM_MAJOR_VERSION
ARG PLUGIN_SWARM_MINOR_VERSION
ARG PLUGIN_SWARM_VERSION
ARG SWARM_JAR_NAME

# GitHub Authentication plugin
ARG PLUGIN_GITHUB_MAJOR_VERSION
ARG PLUGIN_GITHUB_MINOR_VERSION
ARG PLUGIN_GITHUB_VERSION
ARG GITHUB_JAR_NAME

# File Secrets plugin
ARG PLUGIN_FILE_SECRET_VERSION
ARG FILE_SECRET_JAR_NAME

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

# TODO, change to pip install once stable
RUN cd /tmp \
    && git clone https://github.com/rasmunk/gocd-tools.git \
    && cd /tmp/gocd-tools \
    && pip3 install .

USER ${USER}

# Install the docker swarm plugin
RUN wget "https://github.com/gocd-contrib/docker-swarm-elastic-agent-plugin/releases/download/v${PLUGIN_SWARM_VERSION}/${SWARM_JAR_NAME}" -P /tmp/

# Install the GitHub auth plugin
RUN wget "https://github.com/gocd-contrib/github-oauth-authorization-plugin/releases/download/v${PLUGIN_GITHUB_VERSION}/${GITHUB_JAR_NAME}" -P /tmp/

# Install the File secret plugin
RUN wget "https://github.com/gocd/gocd-file-based-secrets-plugin/releases/download/v${PLUGIN_FILE_SECRET_VERSION}/${FILE_SECRET_JAR_NAME}" -P /tmp/

# Create the required diectories
RUN mkdir -p ${GO_PLUGINS_EXTERNAL_DIR} ${GO_PLUGINS_BUNDLED_DIR}
# Move the jars into the plugin directory
RUN mv /tmp/${SWARM_JAR_NAME} ${GO_PLUGINS_EXTERNAL_DIR}/
RUN mv /tmp/${GITHUB_JAR_NAME} ${GO_PLUGINS_EXTERNAL_DIR}/
# Ensure that the file secret plugin is available on the first launch
# even though it will be generated as part of the default bundled
# This makes it available for usage in the docker-entrypoint.d scripts
RUN mv /tmp/${FILE_SECRET_JAR_NAME} ${GO_PLUGINS_BUNDLED_DIR}/

# Ensure that the plugins are available in the path
ENV PATH="${PATH}:${GO_PLUGINS_EXTERNAL_DIR}:${GO_PLUGINS_BUNDLED_DIR}"
