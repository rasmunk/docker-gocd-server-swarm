#!/usr/bin/env python
import requests
import json
from defaults import cluster_profiles_path, elastic_agent_profile_path, repositories_path
from config import load_config


BASE_URL = ""
GO_URL = "{}/go".format(BASE_URL)
API_URL = "{}/api".format(GO_URL)


ELASTIC_AGENT_URL = "{}/elastic/profiles".format(API_URL)
ADMIN_URL = "{}/admin".format(API_URL)
CLUSTER_PROFILES_URL = "{}/elastic/cluster_profiles".format(ADMIN_URL)
CONFIG_REPO_URL = "{}/config_repos".format(ADMIN_URL)


AUTH_TOKEN = ""


def authenticate(session, headers=None):
    if not headers:
        headers = {"Authorization": "bearer {}".format(AUTH_TOKEN),
                   "Accept": "application/vnd.go.cd.v1+json"}
    auth_url = "{}/current_user".format(API_URL)
    return session.get(auth_url, headers=headers)


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
        headers = {"Accept": "application/vnd.go.cd.v1+json",
                   "Content-Type": "application/json"}
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
        headers = {"Accept": "application/vnd.go.cd.v2+json",
                   "Content-Type": "application/json"}
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


def create_config_repo(session, data=None, headers=None):
    if not headers:
        headers = {"Accept": "application/vnd.go.cd.v4+json",
                   "Content-Type": "application/json"}
    if not data:
        data = {}
    json_data = json.dumps(data)
    return post(session, CONFIG_REPO_URL, data=json_data, headers=headers).text


def auth_repo_required(repository_config):
    if "authentication" not in repository_config:
        return False
    if "required" not in repository_config["authentication"]:
        return False
    if not repository_config["authentication"]

    if "required" in repository_config["authentication"]:
        
        return repository_config["authentcation"]["secret"]


if __name__ == "__main__":
    cluster_profiles_config = load_config(path=cluster_profiles_path)
    elastic_agent_config = load_config(path=elastic_agent_profile_path)
    repositories_config = load_config(path=repositories_path)

    if not cluster_profiles_config:
        print("Failed loading: {}".format(cluster_profiles_path))
        exit(1)

    if not elastic_agent_config:
        print("Failed loading: {}".format(elastic_agent_profile_path))
        exit(1)

    if not repositories_config:
        print("Failed loading: {}".format(repositories_path))
        exit(1)

    with requests.Session() as session:
        print("Auth")
        authed = authenticate(session)
        # print(authed.status_code, authed.text)

        print("Cluster profiles")
        # Create cluster profile
        existing_cluster = get_cluster(session, cluster_profiles_config["id"])
        if not existing_cluster:
            created = create_cluster_profile(
                session,
                data=cluster_profiles_config
            )
            if not created:
                print("Failed to create cluster profile: {}".format(cluster_profiles_config))
                exit(1)

        existing_agent = get_elastic_agent(session, elastic_agent_config["id"])
        if not existing_agent:
            created = create_elastic_agent_profile(session, data=elastic_agent_config)
            if not created:
                print("Failed to create elastic agent profile: {}".format(created))
                exit(1)

        print("Config Repositories")
        for repository_config in repositories_config:
            existing_repo = get_config_repo(session, repository_config["id"])
            if not existing_repo:
                # Check whether a secret auth token is required
                extra_config_kwargs = {}
                if auth_repo_required(repository_config):
                    auth_repo_data = extract_auth_data(repository_config)
                    secret = get_secret(auth_repo_data["id"])
                    if not secret:
                        created = create_secret(repository_config)
                        if not created:
                            print("Failed to create new secret")
                        extra_config_kwargs["secret"] = created

                created = create_config_repo(session, data=repository_config, extra_config_kwargs=extra_config_kwargs)
                if not created:
                    print("Failed to create elastic agent profile: {}".format(created))
                    exit(1)
                print(created)
                    

        # Associate GitHub token with the specified repo

        print("Setup SSH keys for private checkouts")

        
        