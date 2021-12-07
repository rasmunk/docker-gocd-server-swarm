#!/usr/bin/python3
import os
from secrets.defaults import GO_SECRET_DIR, GO_PLUGINS_BUNDLED_DIR, GOCD_SECRET_PLUGIN
from secrets.config import load_config
from secrets.utils import path_exists, is_env_set, process


if __name__ == "__main__":
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
