# docker-gocd-server-swarm
A repo for the gocd server with the docker swarm plugin installed


https://api.gocd.org/current/


To authenticate against the GOCD server, a Personal Authentication Token needs to be generate on
the GOCD server. This token needs to be supplied either directly to the `setup_gocd_server.py`
script, or set the `AUTH_TOKEN` environment variable.

In addition, the URL of the GOCD server needs to be supplied to the `setup_gocd_server.py` script
or to the `BASE_URL` environment variable.