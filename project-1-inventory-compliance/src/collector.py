import os
from pathlib import Path

import yaml
from netmiko import ConnectHandler


COMMANDS = {
    "running_config": "show running-config",
    "version": "show version",
    "interfaces": "show ip interface brief",
    "routes": "show ip route",
    "ospf_neighbors": "show ip ospf neighbor",
}


def load_devices(path):
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["devices"]


def collect_device(device):
    #username = os.environ["NET_USERNAME"]
    #password = os.environ["NET_PASSWORD"]
    username = "ennygaebs"
    password = "segelulu96"
    connection_parameters = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": username,
        "password": password,
    }

    connection = ConnectHandler(**connection_parameters)

    results = {}

    try:
        for name, command in COMMANDS.items():
            print(f"  Collecting {command}")
            results[name] = connection.send_command(command)

    finally:
        connection.disconnect()

    return results


def collect_all(devices, raw_directory):
    raw_directory = Path(raw_directory)
    raw_directory.mkdir(parents=True, exist_ok=True)

    collected = {}

    for device in devices:
        print(f"\nConnecting to {device['name']} ({device['host']})")

        try:
            output = collect_device(device)

            collected[device["name"]] = {
                "device": device,
                "output": output,
            }

            device_directory = raw_directory / device["name"]
            device_directory.mkdir(exist_ok=True)

            for command_name, command_output in output.items():
                file_path = device_directory / f"{command_name}.txt"
                file_path.write_text(
                    command_output,
                    encoding="utf-8",
                )

            print(f"  ✓ {device['name']} collected successfully")

        except Exception as error:
            print(f"  ✗ {device['name']} failed: {error}")

    return collected  



#devices = load_devices("project-1-inventory-compliance/devices.yaml")
#BASE_DIR = Path(__file__).resolve().parent

#INVENTORY_FILE = BASE_DIR / "devices.yaml"
#BASELINE_FILE = BASE_DIR / "baseline.yaml"

#RAW_DIRECTORY = BASE_DIR / "data" / "raw"
#REPORTS_DIRECTORY = BASE_DIR / "reports"
#collect_all(devices,RAW_DIRECTORY)
