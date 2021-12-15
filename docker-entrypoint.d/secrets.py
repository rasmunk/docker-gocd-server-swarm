import subprocess
import json


def run_command(command):
    result = subprocess.run(init_command)
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


if __name__ == "__main__":
    print("Run gocd-tools secrets init")
    init_command = ["gocd-tools", "setup", "secrets", "init"]
    result = run_command(init_command)

    init_output_json = json.dumps(result["stdout"])
    if init_output_json["status"] != "success":
        print("Failed command: {}".format(init_command))
        print(init_output_json)

    print("Run gocd-tools secrets configure")
    configure_command = ["gocd-tools", "setup", "secrets", "configure"]
    conf_result = run_command(configure_command)

    conf_output_json = json.dumps(conf_result["stdout"])
    if conf_output_json["status"] != "success":
        print("Failed command: {}".format(configure_command))
        print(conf_output_json)
