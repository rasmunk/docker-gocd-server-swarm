#!/usr/bin/python3
import argparse
import os
import json
from secrets.defaults import (
    GO_SECRET_DIR,
    GO_PLUGINS_BUNDLED_DIR,
    GOCD_SECRET_PLUGIN,
    PACKAGE_NAME,
    get_secrets_dir_path,
    get_secrets_db_path,
)
from secrets.config import load_config
from secrets.io import remove, makedirs, exists
from secrets.utils import path_exists, is_env_set, process, eprint, to_str


def add_cleanup_input(parser):
    cleanup_group = parser.add_argument_group(title="Cleanup arguments")
    cleanup_group.add_argument("--remove-input-secretdb", type=bool, default=False)



def run_cli():
    parser = argparse.ArgumentParser(prog=PACKAGE_NAME)
    commands = parser.add_subparsers("COMMAND")
    cleanup_parser = commands.add_parser("cleanup")
    add_cleanup_input(cleanup_parser)
    cleanup_parser.set_defaults(func=cleanup_secrets_db)

    args = parser.parse_args()
    if hasattr(args, "func"):
        success, response = args.func(args)
        output = ""
        if success:
            response["status"] = "success"
        else:
            response["status"] = "failed"

        try:
            output = json.dumps(response, indent=4, sort_keys=True, default=to_str)
        except Exception as err:
            eprint("Failed to format: {}, err: {}".format(output, err))
        if success:
            print(output)
        else:
            eprint(output)
    return None


def init_secrets_dir():
    response = {}
    secrets_dir_path, msg = get_secrets_dir_path()
    if not secret_dir_path:
        response["msg"] = msg
        return False, response

    if not exists(secrets_dir_path):
        # Ensure the secrets dir is there
        created, msg = makedirs(secrets_dir_path)
        response["msg"] = msg
        if not created:
            return False, response
        return True, response

    response["msg"] = "The secrets db directory already exists: {}".format(
        secrets_dir_path
    )
    return True, response


def secrets_db_exist():
    response = {}
    db_path, msg = get_secrets_db_path()
    if not db_path:
        response["msg"] = msg
        return False, response
    return exists(db_path), ""


def cleanup_secrets_db():
    response = {}

    db_path, msg = get_secrets_db_path()
    if not db_path:
        response["msg"] = msg
        return False, response

    if not exists(db_path):
        response["msg"] = "The db path: {} does not exist".format(db_path)
        return True, response

    removed, msg = remove(db_path)
    response["msg"] = msg
    if not removed:
        return False, response
    return True, response


if __name__ == "__main__":
    run = run_cli()

    bundled_plugin_path = os.environ[GO_PLUGINS_BUNDLED_DIR]
    if not is_env_set(GO_PLUGINS_BUNDLED_DIR, bundled_plugin_path):
        exit(1)

    if not path_exists(bundled_plugin_path):
        exit(1)

    file_secret_plugin_path = os.path.join(bundled_plugin_path, GOCD_SECRET_PLUGIN)
    if not path_exists(file_secret_plugin_path):
        exit(1)

    secret_dir_path = os.environ[GO_SECRET_DIR]
    if not is_env_set(GO_SECRET_DIR, secret_dir_path):
        exit(1)

    if not path_exists(secret_dir_path):
        exit(1)

    secrets_db_config_path = os.path.join(GO_SECRET_DIR, "secrets.yml")
    if not path_exists(secrets_db_config_path):
        exit(1)

    secret_db = load_config(secrets_db_config_path)
    if not secret_db:
        print("Failed loading: {}".format(secrets_db_config_path))
        exit(1)

    # Initialize the secret DBs
    base_plugin_cmd = ["java", "-jar", file_secret_plugin_path]
    print("Base plugin cmd: {}".format(base_plugin_cmd))
    create_db_cmd = base_plugin_cmd + ["init", "-f"]
    print("Create_db_cmd: {}".format(create_db_cmd))

    # Add the secret key and values to the secret dbs
    base_add_secret_cmd = base_plugin_cmd + ["add", "-f"]
    for secret_db_key, secret_db in secret_db.items():
        # Create the secret db if it doesn't exist
        if not os.path.exists(secret_db["path"]):
            new_db_cmd = create_db_cmd + [secret_db["path"]]
            execute_kwargs = {"commands": [new_db_cmd], "capture": True}
            result = process(execute_kwargs=execute_kwargs)
            print("Result: {}".format(result))

        # Assign the 'data' key in the secret_db to the secret file
        db_add_cmd = base_add_secret_cmd + [secret_db["path"]]
        for key, value in secret_db["data"].items():
            add_secret_cmd = db_add_cmd + ["-n", key, "-v", value]
            execute_kwargs = {"commands": [add_secret_cmd], "capture": True}
            result = process(execute_kwargs=execute_kwargs)
            print("Result: {}".format(result))

    # TODO, have an optional flag for deleting the secret input db after setup
