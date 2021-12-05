import os

PACKAGE_NAME = "gocd-utils"

default_base_path = os.path.join(os.path.expanduser("~"), ".{}".format(PACKAGE_NAME))
default_config_path = os.path.join(default_base_path, "config")

cluster_profiles_path = os.path.join(default_config_path, "cluster_profiles.yml")
elastic_agent_profile_path = os.path.join(
    default_config_path, "elastic_agent_profiles.yml"
)
repositories_path = os.path.join(default_config_path, "repositories.yml")
authorization_config_path = os.path.join(default_config_path, "authorization.yml")
secret_managers_config_path = os.path.join(default_config_path, "secret_managers.yml")


# API Request Defaults
CONTENT_TYPE = "application/json"
JSON_HEADER = {"Content-Type": CONTENT_TYPE}

API_VERSION_1 = "application/vnd.go.cd.v1+json"
API_VERSION_2 = "application/vnd.go.cd.v2+json"
API_VERSION_3 = "application/vnd.go.cd.v3+json"
API_VERSION_4 = "application/vnd.go.cd.v4+json"

ACCEPT_HEADER_1 = {"Accept": API_VERSION_1, **JSON_HEADER}
ACCEPT_HEADER_2 = {"Accept": API_VERSION_2, **JSON_HEADER}
ACCEPT_HEADER_3 = {"Accept": API_VERSION_3, **JSON_HEADER}
ACCEPT_HEADER_4 = {"Accept": API_VERSION_4, **JSON_HEADER}
