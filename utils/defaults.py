import os

PACKAGE_NAME = "gocd-utils"

default_base_path = os.path.join(os.path.expanduser("~"), ".{}".format(PACKAGE_NAME))

cluster_profiles_path = os.path.join(default_base_path, "cluster_profiles.yml")
elastic_agent_profile_path = os.path.join(default_base_path, "elastic_agent_profile.yml")
repositories_path = os.path.join(default_base_path, "repositories.yml")
