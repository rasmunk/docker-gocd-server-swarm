import os

PACKAGE_NAME = "gocd-utils"

default_base_path = os.path.join(os.path.expanduser("~"), ".{}".format(PACKAGE_NAME))
default_config_path = os.path.join(default_base_path, "config")

cluster_profiles_path = os.path.join(default_config_path, "cluster_profiles.yml")
elastic_agent_profile_path = os.path.join(
    default_config_path, "elastic_agent_profiles.yml"
)
repositories_path = os.path.join(default_config_path, "repositories.yml")
