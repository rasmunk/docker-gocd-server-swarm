#!/usr/bin/python3
import os
import subprocess
import inspect

# ENV variables
GO_PLUGINS_BUNDLED_DIR = "GO_PLUGINS_BUNDLED_DIR"
GO_SECRET_DIR = "GO_SECRET_DIR"

# Other constants
GOCD_SECRET_PLUGIN = "gocd-file-based-secrets-plugin.jar"


def is_env_set(name, value):
    if not value:
        print("The required environment variable: {} is not set".format(name))
        return False
    return True

def path_exists(path):
    if not os.path.exists(path):
        print("The path: {} does not exist".format(path))
        return False
    return True


def process(execute_kwargs=None):
    """ Function for execute a set of command lines"""
    if not execute_kwargs:
        execute_kwargs = {}

    print("Execute Kwargs: {}".format(execute_kwargs))
    commands = execute_kwargs["commands"]
    if not isinstance(commands, list):
        commands = [execute_kwargs["commands"]]

    output_results = []
    for command in commands:
        if isinstance(command, str):
            prepared_command = command.split()
        elif isinstance(command, list):
            prepared_command = command
        else:
            raise TypeError("Incorrect command type handed to process")
        # Subprocess
        run_kwargs = {}
        available_arguments = inspect.getfullargspec(subprocess.run)
        if "capture_output" in available_arguments.kwonlyargs and "capture" in execute_kwargs:
            run_kwargs["capture_output"] = execute_kwargs["capture"]
        else:
            if execute_kwargs["capture"]:
                run_kwargs["stdout"] = subprocess.PIPE
                run_kwargs["stderr"] = subprocess.PIPE

        result = subprocess.run(prepared_command, **run_kwargs)
        command_results = {}
        if hasattr(result, "args"):
            command_results.update({"command": " ".join((getattr(result, "args")))})
        if hasattr(result, "returncode"):
            command_results.update({"returncode": str(getattr(result, "returncode"))})
        if hasattr(result, "stderr"):
            command_results.update({"error": str(getattr(result, "stderr"))})
        if hasattr(result, "stdout"):
            command_results.update({"output": str(getattr(result, "stdout"))})
        output_results.append(command_results)
    return output_results


bundled_plugin_path = os.environ[GO_PLUGINS_BUNDLED_DIR]
if not is_env_set(GO_PLUGINS_BUNDLED_DIR, bundled_plugin_path):
    exit(1)

if not path_exists(bundled_plugin_path):
    exit(1)

file_secret_plugin_path = os.path.join(bundled_plugin_path, GOCD_SECRET_PLUGIN)
if not path_exists(file_secret_plugin_path):
    exit(2)

secret_dir_path = os.environ[GO_SECRET_DIR]
if not is_env_set(GO_SECRET_DIR, secret_dir_path):
    exit(1)

if not path_exists(secret_dir_path):
    exit(2)

# TODO, move the data to an external secret yaml file that is supplied by ansible
secret_db = {}

# Initialize the secret DBs
base_plugin_cmd = ["java", "-jar", file_secret_plugin_path]
print("Base plugin cmd: {}".format(base_plugin_cmd))
create_db_cmd = base_plugin_cmd + ["init", "-f"]
print("Create_db_cmd: {}".format(create_db_cmd))

# Add the secret key and values to the secret dbs
base_add_secret_cmd = base_plugin_cmd + ["add", '-f']
for secret_db_key, secret_db in secret_db.items():
    # Create the secret db if it doesn't exist
    if not os.path.exists(secret_db["path"]):
        new_db_cmd = create_db_cmd + [secret_db["path"]]
        execute_kwargs = {"commands": [new_db_cmd],
                          "capture": True}
        result = process(execute_kwargs=execute_kwargs)
        print("Result: {}".format(result))

    # Assign the 'data' key in the secret_db to the secret file
    db_add_cmd = base_add_secret_cmd + [secret_db["path"]]
    for key, value in secret_db["data"].items():
        add_secret_cmd = db_add_cmd + ["-n", key, "-v", value]
        execute_kwargs = {"commands": [add_secret_cmd], "capture": True}
        result = process(execute_kwargs=execute_kwargs)
        print("Result: {}".format(result))
