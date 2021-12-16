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


def ensure_string(value):
    return_value = None
    if isinstance(value, bytes):
        return_value = value.decode("utf-8")
    if isinstance(value, str):
        # Ensure utf-8 encoding
        return_value = value.encode("utf-8")
    if isinstance(value, int):
        return_value = str(value)
    return return_value


def format_output_json(result):
    json_result = {}
    for key, value in result.items():
        try:
            evalued = literal_eval(value)
        except SyntaxError:
            # still try to encode it correctly
            string_value = ensure_string(value)
            json_result[key] = string_value
            continue

        string_evalued = ensure_string(evalued)
        if len(string_evalued) > 0:
            try:
                json_result[key] = json.loads(string_evalued)
            except Exception:
                json_result[key] = string_evalued
        else:
            json_result[key] = string_evalued
    return json_result


def print_output(json_result):
    if "status" in json_result["error"] and json_result["error"]["status"] == "failed":
        if "msg" in json_result["error"]:
            print("Error: {}".format(json_result["error"]["msg"]))
        else:
            print("Error: {}".format(json_result))
    print(json_result["output"])
