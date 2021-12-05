#!/usr/bin/env python
import os
import requests
import json
from defaults import (
    authorization_config_path,
    cluster_profiles_path,
    elastic_agent_profile_path,
    repositories_path,
    secret_managers_config_path,
    JSON_HEADER,
    ACCEPT_HEADER_1,
    ACCEPT_HEADER_2,
    ACCEPT_HEADER_3,
    ACCEPT_HEADER_4,
)
from config import load_config


if "BASE_URL" in os.environ:
    BASE_URL = os.environ["BASE_URL"]
else:
    BASE_URL = ""

# Public URLs
GO_URL = "{}/go".format(BASE_URL)
API_URL = "{}/api".format(GO_URL)

AUTH_URL = "{}/current_user".format(API_URL)
ELASTIC_AGENT_URL = "{}/elastic/profiles".format(API_URL)
ADMIN_URL = "{}/admin".format(API_URL)
SECURITY_URL = "{}/security".format(ADMIN_URL)

# Restricted URLs
AUTHORIZATION_CONFIG_URL = "{}/auth_configs".format(SECURITY_URL)
CLUSTER_PROFILES_URL = "{}/elastic/cluster_profiles".format(ADMIN_URL)
CONFIG_REPO_URL = "{}/config_repos".format(ADMIN_URL)
SECRET_CONFIG_URL = "{}/secret_configs".format(ADMIN_URL)

if "AUTH_TOKEN" in os.environ:
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
else:
    AUTH_TOKEN = ""
    # The AUTH_TOKEN is the one generate within the GOCD server
    # (Not GitHub)

AUTHORIZATION_HEADER = {
    "Authorization": "bearer {}".format(AUTH_TOKEN),
    **ACCEPT_HEADER_1,
}


def get(session, url, *args, **kwargs):
    try:
        return session.get(url, *args, **kwargs)
    except Exception as err:
        print("Failed GET request: {}".format(err))
    return None


def post(session, url, *args, **kwargs):
    try:
        return session.post(url, *args, **kwargs)
    except Exception as err:
        print("Failed POST request: {}".format(err))
    return None


def get_type(session, base_url, id, headers=None):
    id_url = "{}/{}".format(base_url, id)
    resp = get(session, id_url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    return None


def get_types(session, base_url, headers=None):
    resp = get(session, base_url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    return None


def create_type(session, url, data=None, headers=None):
    json_data = json.dumps(data)
    created = post(session, url, data=json_data, headers=headers)
    if created.status_code == 200:
        return True
    print("Failed to create type: {}".format(created.text))
    return False


def authenticate(session):
    resp = get(session, AUTH_URL, headers=AUTHORIZATION_HEADER)
    if resp.status_code == 200:
        return True
    return False


def is_auth_repo(repository_config):
    if "authentication" not in repository_config:
        return False
    if "required" not in repository_config["authentication"]:
        return False
    if not repository_config["authentication"]["required"]:
        return False
    return True


def repo_auth_data(repository_config):
    return repository_config["authentication"]


def get_repo_secret(auth_data):
    if "secret" not in auth_data:
        return False
    return auth_data["secret"]


def get_repo_secret_manager(repository_config):
    return repository_config["authentication"]["secret_plugin"]


def get_secret_configs(session, headers=None):
    if not headers:
        headers = ACCEPT_HEADER_3
    return get(session, SECRET_CONFIG_URL)

def get_secret_manager(session, id):
    return get_type(session, SECRET_CONFIG_URL, id, headers=ACCEPT_HEADER_3)


if __name__ == "__main__":
    cluster_profiles_configs = load_config(path=cluster_profiles_path)
    elastic_agent_configs = load_config(path=elastic_agent_profile_path)
    repositories_configs = load_config(path=repositories_path)
    # TODO, load and create the authorization config
    authorization_configs = load_config(path=authorization_config_path)
    secret_managers_configs = load_config(path=secret_managers_config_path)

    configs = [
        {"path": cluster_profiles_path, "config": cluster_profiles_configs},
        {"path": elastic_agent_profile_path, "config": elastic_agent_configs},
        {"path": repositories_path, "config": repositories_configs},
        {"path": secret_managers_config_path, "config": secret_managers_configs},
        {"path": authorization_config_path, "config": authorization_configs},
    ]

    for config in configs:
        if not config["config"]:
            print("Failed loading: {}".format(config["path"]))
            exit(1)

    with requests.Session() as session:
        print("Authenticate")
        authed = authenticate(session)
        if not authed:
            exit(2)

        print("Setup Authorization config")
        for auth_config in authorization_configs:
            exists = get_type(
                session,
                AUTHORIZATION_CONFIG_URL,
                auth_config["id"],
                headers=ACCEPT_HEADER_2,
            )
            if not exists:
                created = create_type(
                    session,
                    AUTHORIZATION_CONFIG_URL,
                    data=auth_config,
                    headers=ACCEPT_HEADER_2,
                )
                if not created:
                    print(
                        "Failed to create authorization config: {}".format(auth_config)
                    )
                    exit(4)

        print("Setup Secret Manager")
        for secret_manager_config in secret_managers_configs:
            exists = get_type(
                session,
                SECRET_CONFIG_URL,
                secret_manager_config["id"],
                headers=ACCEPT_HEADER_3,
            )
            if not exists:
                created = create_type(
                    session,
                    SECRET_CONFIG_URL,
                    data=secret_manager_config,
                    headers=ACCEPT_HEADER_3,
                )
                if not created:
                    print(
                        "Failed to create secret config: {}".format(
                            secret_manager_config
                        )
                    )
                    exit(5)

        print("Setup Cluster profiles")
        # Create cluster profile
        for cluster_config in cluster_profiles_configs:
            existing_cluster = get_type(
                session,
                CLUSTER_PROFILES_URL,
                cluster_config["id"],
                headers=ACCEPT_HEADER_1,
            )
            if not existing_cluster:
                created = create_type(
                    session,
                    CLUSTER_PROFILES_URL,
                    data=cluster_config,
                    headers=ACCEPT_HEADER_1,
                )
                if not created:
                    print("Failed to create cluster profile: {}".format(cluster_config))
                    exit(6)

        for agent_config in elastic_agent_configs:
            existing_agent = get_type(
                session, ELASTIC_AGENT_URL, agent_config["id"], headers=ACCEPT_HEADER_2
            )
            if not existing_agent:
                created = create_type(
                    session,
                    ELASTIC_AGENT_URL,
                    data=agent_config,
                    headers=ACCEPT_HEADER_2,
                )
                if not created:
                    print("Failed to create elastic agent profile: {}".format(created))
                    exit(7)

        print("Create Config Repositories")
        for repository_config in repositories_configs:
            existing_repo = get_type(
                session,
                CONFIG_REPO_URL,
                repository_config["id"],
                headers=ACCEPT_HEADER_4,
            )
            if not existing_repo:
                # Check whether a secret auth token is required
                extra_config_kwargs = {}
                if is_auth_repo(repository_config):
                    repo_auth_data = repo_auth_data(repository_config)
                    repo_secret_manager = get_repo_secret_manager(repository_config)
                    secret = get_repo_secret(repo_auth_data)

                    secret_manager = get_secret_manager(session, repo_secret_manager)
                    if not secret_manager:
                        print(
                            "Repo: {} tries to use secret manager: {} which doesn't exist".format(
                                repository_config["id"], repo_secret_manager
                            )
                        )
                    # secret = get_type(session, SECRET_CONFIG_URL)
                    # if not secret:
                    # created = create_secret(repository_config)
                    #    created = create_secret(repository_config)
                    #    if not created:
                    #        print("Failed to create new secret")
                    #    extra_config_kwargs["secret"] = created
                created = create_type(
                    session,
                    CONFIG_REPO_URL,
                    data={"id": repository_config["id"], **repository_config["config"]},
                    headers=ACCEPT_HEADER_4,
                )
                if not created:
                    print("Failed to create repository config: {}".format(created))
                    exit(1)
