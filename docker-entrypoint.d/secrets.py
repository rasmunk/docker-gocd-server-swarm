#!/usr/bin/python3
import subprocess
import inspect
import json
from ast import literal_eval


def run_command(command, execute_kwargs=None):
    run_kwargs = {}
    available_arguments = inspect.getfullargspec(subprocess.run)
    if "capture_output" in available_arguments.kwonlyargs:
        run_kwargs["capture_output"] = execute_kwargs["capture"]
    else:
        if execute_kwargs["capture"]:
            run_kwargs["stdout"] = subprocess.PIPE
            run_kwargs["stderr"] = subprocess.PIPE

    result = subprocess.run(command, **run_kwargs)
    command_results = {}
    if hasattr(result, "args"):
        command_results.update({"command": " ".join((getattr(result, "args")))})
    if hasattr(result, "returncode"):
        command_results.update({"returncode": str(getattr(result, "returncode"))})
    if hasattr(result, "stderr"):
        command_results.update({"error": str(getattr(result, "stderr"))})
    if hasattr(result, "stdout"):
        command_results.update({"output": str(getattr(result, "stdout"))})
    return command_results


def format_output_json(result):
    json_result = {}
    for key, value in result.items():
        if key != "command":
            evalued = literal_eval(value)
            if isinstance(evalued, bytes):
                evalued = evalued.decode("utf-8")
            if isinstance(evalued, str):
                # Ensure utf-8 encoding
                evalued = evalued.encode("utf-8")
            if isinstance(evalued, int):
                evalued = str(evalued)

            if len(evalued) > 0:
                json_result[key] = json.loads(evalued)
            else:
                json_result[key] = value
    return json_result


if __name__ == "__main__":
    print("Run gocd-tools secrets init")
    init_command = ["gocd-tools", "setup", "secrets", "init"]
    result = run_command(init_command, execute_kwargs={"capture": True})

    json_result = format_output_json(result)
    if len(json_result["error"]) > 0:
        print("Failed command: {}".format(init_command))
        print(json_result["error"]["msg"])

    print("Run gocd-tools secrets configure")
    configure_command = ["gocd-tools", "setup", "secrets", "configure"]
    conf_result = run_command(configure_command)

    conf_output_json = format_output_json(conf_result)
    if len(conf_output_json["error"]) > 0:
        print("Failed command: {}".format(configure_command))
        print(conf_output_json["error"]["msg"])
