import os
import sys
import subprocess
import inspect


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
    """Function for execute a set of command lines"""
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
        if (
            "capture_output" in available_arguments.kwonlyargs
            and "capture" in execute_kwargs
        ):
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


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)