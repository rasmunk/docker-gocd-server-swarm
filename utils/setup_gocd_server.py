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
    ACCEPT_HEADER_4
)
from config import load_config


if "BASE_URL" in os.environ:
    BASE_URL = os.environ["BASE_URL"]
else:
    BASE_URL = "https://mechanist.rasmunk.dk"

# Public URLs
GO_URL = "{}/go".format(BASE_URL)
API_URL = "{}/api".format(GO_URL)

AUTH_URL = "{}/current_user".format(API_URL)
ELASTIC_AGENT_URL = "{}/elastic/profiles".format(API_URL)
ADMIN_URL = "{}/admin".format(API_URL)

# Restricted URLs
CLUSTER_PROFILES_URL = "{}/elastic/cluster_profiles".format(ADMIN_URL)
CONFIG_REPO_URL = "{}/config_repos".format(ADMIN_URL)
SECRET_CONFIG_URL = "{}/secret_configs".format(ADMIN_URL)

if "AUTH_TOKEN" in os.environ:
    AUTH_TOKEN = os.environ["AUTH_TOKEN"]
else:
    AUTH_TOKEN = "e657c2526dd045c16a0a18104983073044aad222"
    # The AUTH_TOKEN is the one generate within the GOCD server
    # (Not GitHub)

AUTHORIZATION_HEADER = {"Authorization": "bearer {}".format(AUTH_TOKEN), **ACCEPT_HEADER_1}

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
    return post(session, url, data=json_data, headers=headers).text


def authenticate(session):
    resp = get(session, AUTH_URL, headers=AUTHORIZATION_HEADER)
    if resp.status_code == 200:
        return True
    return False

def get_cluster_profiles(session, headers=None):
    if not headers:
        headers = {"Accept": "application/vnd.go.cd.v1+json"}
    return get(session, CLUSTER_PROFILES_URL, headers=headers).text


def get_cluster(session, id, headers=None):
    if not headers:
        headers = {"Accept": "application/vnd.go.cd.v1+json"}
    id_url = "{}/{}".format(CLUSTER_PROFILES_URL, id)
    resp = get(session, id_url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    return None


def create_cluster_profile(session, data=None, headers=None):
    if not headers:
        headers = {
            "Accept": "application/vnd.go.cd.v1+json",
            "Content-Type": CONTENT_TYPE,
        }
    if not data:
        data = {}
    json_data = json.dumps(data)
    return post(session, CLUSTER_PROFILES_URL, data=json_data, headers=headers).text


def get_elastic_agent_profiles(session, headers=None):
    if not headers:
        headers = {"Accept": "application/vnd.go.cd.v2+json"}
    return get(session, ELASTIC_AGENT_URL, headers=headers).text


def get_elastic_agent(session, id, headers=None):
    if not headers:
        headers = {"Accept": "application/vnd.go.cd.v2+json"}
    id_url = "{}/{}".format(ELASTIC_AGENT_URL, id)
    resp = get(session, id_url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    return None


def create_elastic_agent_profile(session, data=None, headers=None):
    if not headers:
        headers = {
            "Accept": "application/vnd.go.cd.v2+json",
            "Content-Type": CONTENT_TYPE,
        }
    if not data:
        data = {}
    json_data = json.dumps(data)
    return post(session, ELASTIC_AGENT_URL, data=json_data, headers=headers).text


def get_config_repo(session, id, headers=None):
    if not headers:
        headers = {"Accept": "application/vnd.go.cd.v4+json"}
    id_url = "{}/{}".format(CONFIG_REPO_URL, id)
    resp = get(session, id_url, headers=headers)
    if resp.status_code == 200:
        return resp.text
    return None


def create_config_repo(session, config_id=None, data=None, headers=None, extra_config_kwargs=None):
    if not headers:
        headers = {
            "Accept": "application/vnd.go.cd.v4+json",
            "Content-Type": CONTENT_TYPE,
        }
    if not data:
        data = {}

    request_data = {"id": config_id, **data}
    json_data = json.dumps(request_data)
    return post(session, CONFIG_REPO_URL, data=json_data, headers=headers).text


def is_auth_repo(repository_config):
    if "authentication" not in repository_config:
        return False
    if "required" not in repository_config["authentication"]:
        return False
    if not repository_config["authentication"]["required"]:
        return False
    return True


def extract_auth_data(repository_config):
    return repository_config["authentication"]

def get_secret(auth_data):
    if "secret" not in auth_data:
        return False
    return auth_data["secret"]


def get_repo_secret_manager(repository_config):
    return repository_config["authentication"]["secret_plugin"]


def get_secret_configs(session, headers=None):
    if not headers:
        headers = ACCEPT_HEADER_3
    return get(session, SECRET_CONFIG_URL)


def create_secret_config(session, data=None, headers=None):
    if not headers:
        headers = ACCEPT_HEADER_3
    if not data:
        data = {}
    json_data = json.dumps(data)
    return post(session, SECRET_CONFIG_URL, data=json_data, headers=headers).text


if __name__ == "__main__":
    cluster_profiles_config = load_config(path=cluster_profiles_path)
    elastic_agent_config = load_config(path=elastic_agent_profile_path)
    repositories_config = load_config(path=repositories_path)
    # TODO, load and create the authorization config
    authorization_config = load_config(path=authorization_config_path)
    secret_managers_config = load_config(path=secret_managers_config_path)

    configs = [
        {"path": cluster_profiles_path, "config": cluster_profiles_config},
        {"path": elastic_agent_profile_path, "config": elastic_agent_config},
        {"path": repositories_path, "config": repositories_config},
        {"path": secret_managers_config_path, "config": secret_managers_config},
        {"path": authorization_config_path, "config": authorization_config}
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

#        print("Setup Authorization config")


        print("Setup Secret Manager")
        for secret_manager_config in secret_managers_config:
            exists = get_type(session, SECRET_CONFIG_URL, secret_manager_config["id"], headers=ACCEPT_HEADER_4)
#            exists = get_secret_config(session, secret_manager_config["id"])
            if not exists:
                created = create_type(session, SECRET_CONFIG_URL, data=secret_manager_config, headers=ACCEPT_HEADER_3)
                # created = create_secret_config(session, data=secret_manager_config)
                if not created:
                    print("Failed to create secret config: {}".format(
                        secret_manager_config
                    ))
                    exit(3)

        print("Setup Cluster profiles")
        # Create cluster profile
        #existing_cluster = get_cluster(session, cluster_profiles_config["id"])
        existing_cluster = get_type(session, CLUSTER_PROFILES_URL, cluster_profiles_config["id"], headers=ACCEPT_HEADER_1)
        if not existing_cluster:
            #created = create_cluster_profile(session, data=cluster_profiles_config)
            created = create_type(session, CLUSTER_PROFILES_URL, data=cluster_profiles_config, headers=ACCEPT_HEADER_1)
            if not created:
                print(
                    "Failed to create cluster profile: {}".format(
                        cluster_profiles_config
                    )
                )
                exit(4)

        #existing_agent = get_elastic_agent(session, elastic_agent_config["id"])
        existing_agent = get_type(session, ELASTIC_AGENT_URL, elastic_agent_config["id"], headers=ACCEPT_HEADER_2)
        if not existing_agent:
            #created = create_elastic_agent_profile(session, data=elastic_agent_config)
            created = create_type(session, ELASTIC_AGENT_URL, data=elastic_agent_config, headers=ACCEPT_HEADER_2)
            if not created:
                print("Failed to create elastic agent profile: {}".format(created))
                exit(5)

        print("Create Config Repositories")
        for repository_config in repositories_config:
            #existing_repo = get_config_repo(session, repository_config["id"])
            existing_repo = get_type(session, CONFIG_REPO_URL, repository_config["id"], headers=ACCEPT_HEADER_4)
            if not existing_repo:
                # Check whether a secret auth token is required
                extra_config_kwargs = {}
                if is_auth_repo(repository_config):
                    auth_data = extract_auth_data(repository_config)
                    secret_manager = get_secret_manager(repository_config)
                    secret = get_secret(auth_data)
                    if not secret:
                        #created = create_secret(repository_config)
                        created = create_secret(repository_config)
                        if not created:
                            print("Failed to create new secret")
                        extra_config_kwargs["secret"] = created

                created = create_config_repo(
                    session,
                    config_id=repository_config["id"],
                    data=repository_config["config"],
                    extra_config_kwargs=extra_config_kwargs,
                )
                if not created:
                    print("Failed to create elastic agent profile: {}".format(created))
                    exit(1)
                print(created)

        # Associate GitHub token with the specified repo
        print("Setup SSH keys for private checkouts")
