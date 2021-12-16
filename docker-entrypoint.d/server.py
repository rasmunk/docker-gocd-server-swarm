#!/usr/bin/python3
from setup.utils import run_command, format_output_json, print_output

if __name__ == "__main__":
    print("Run gocd-tools server init")
    init_command = ["gocd-tools", "setup", "server", "init"]
    result = run_command(init_command, execute_kwargs={"capture": True})

    json_result = format_output_json(result)
    print_output(json_result)

    print("Run gocd-tools server configure")
    configure_command = ["gocd-tools", "setup", "server", "configure"]
    result = run_command(configure_command, execute_kwargs={"capture": True})

    json_result = format_output_json(result)
    print_output(json_result)
