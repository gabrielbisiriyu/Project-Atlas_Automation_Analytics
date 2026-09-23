import re

import pandas as pd


def parse_version(output, device):
    hostname_match = re.search(
        r"(?m)^(\S+)\s+uptime is",
        output,
    )

    version_match = re.search(
        r"Cisco IOS(?: XE)? Software.*?Version\s+([^,\s]+)",
        output,
        re.IGNORECASE | re.DOTALL,
    )

    hostname = (
        hostname_match.group(1)
        if hostname_match
        else device["name"]
    )

    version = (
        version_match.group(1)
        if version_match
        else "Unknown"
    )

    return {
        "hostname": hostname,
        "management_ip": device["host"],
        "role": device["role"],
        "ios_version": version,
    }


def parse_interfaces(output, device_name):
    rows = []

    for line in output.splitlines():
        line = line.strip()

        if not line or line.startswith("Interface"):
            continue

        parts = line.split()

        if len(parts) < 6:
            continue

        interface = parts[0]
        ip_address = parts[1]
        status = parts[-2]
        protocol = parts[-1]

        rows.append({
            "device": device_name,
            "interface": interface,
            "ip_address": ip_address,
            "status": status,
            "protocol": protocol,
        })

    return rows


def parse_routes(output, device_name):
    rows = []

    for line in output.splitlines():
        line = line.strip()

        if not line or line.startswith("Codes:"):
            continue

        match = re.search(
            r"^([A-Z*])\s+(\S+).*",
            line,
        )

        if match:
            rows.append({
                "device": device_name,
                "protocol": match.group(1),
                "route": match.group(2),
                "raw": line,
            })

    return rows


def parse_ospf_neighbors(output, device_name):
    rows = []

    for line in output.splitlines():
        line = line.strip()

        if not line or line.startswith("Neighbor"):
            continue

        parts = line.split()

        if len(parts) >= 6:
            rows.append({
                "device": device_name,
                "neighbor_id": parts[0],
                "priority": parts[1],
                "state": parts[2],
                "dead_time": parts[3],
                "address": parts[4],
                "interface": parts[5],
            })

    return rows


def build_dataframes(collected):
    inventory_rows = []
    interface_rows = []
    route_rows = []
    ospf_rows = []

    for device_name, data in collected.items():
        device = data["device"]
        output = data["output"]

        inventory_rows.append(
            parse_version(
                output["version"],
                device,
            )
        )

        interface_rows.extend(
            parse_interfaces(
                output["interfaces"],
                device_name,
            )
        )

        route_rows.extend(
            parse_routes(
                output["routes"],
                device_name,
            )
        )

        ospf_rows.extend(
            parse_ospf_neighbors(
                output["ospf_neighbors"],
                device_name,
            )
        )

    return {
        "inventory": pd.DataFrame(inventory_rows),
        "interfaces": pd.DataFrame(interface_rows),
        "routes": pd.DataFrame(route_rows),
        "ospf_neighbors": pd.DataFrame(ospf_rows),
    }