import re
from pathlib import Path

import pandas as pd


SYSLOG_PATTERN = re.compile(
    r"^(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<device>\S+)\s+"
    r"(?P<sequence>\d+):\s+"
    r"\*(?P<device_timestamp>[A-Z][a-z]{2}\s+\d+\s+"
    r"\d{2}:\d{2}:\d{2}\.\d+):\s+"
    r"%(?P<facility>[A-Z0-9_-]+)-(?P<severity>\d+)-"
    r"(?P<mnemonic>[A-Z0-9_-]+):\s+"
    r"(?P<message>.*)$"
)


def parse_log_line(line):
    match = SYSLOG_PATTERN.match(line.strip())

    if not match:
        return None

    event = match.groupdict()

    event["severity"] = int(event["severity"])

    message = event["message"]

    event["event_type"] = classify_event(
        event["facility"],
        event["mnemonic"],
        message,
    )

    event["username"] = extract_username(message)
    event["source_ip"] = extract_source_ip(message)

    ospf_data = extract_ospf_details(message)

    event.update(ospf_data)

    return event


def classify_event(facility, mnemonic, message):
    if facility == "SYS" and mnemonic == "CONFIG_I":
        return "configuration_change"

    if facility == "OSPF" and mnemonic == "ADJCHG":
        return "ospf_adjacency_change"

    if "AUTH" in mnemonic or "authentication" in message.lower():
        return "authentication_event"

    if "LINK" in mnemonic or "LINEPROTO" in facility:
        return "interface_event"

    return "other"


def extract_username(message):
    match = re.search(
        r"\bby\s+(\S+)\s+on\s+(?:vty\d+|console)",
        message,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None


def extract_source_ip(message):
    match = re.search(
        r"\((\d+\.\d+\.\d+\.\d+)\)",
        message,
    )

    if match:
        return match.group(1)

    return None


def extract_ospf_details(message):
    result = {
        "ospf_neighbor": None,
        "ospf_interface": None,
        "ospf_old_state": None,
        "ospf_new_state": None,
        "ospf_reason": None,
    }

    match = re.search(
        r"Nbr\s+(\S+)\s+on\s+(\S+)\s+from\s+(\S+)\s+to\s+(\S+),\s+"
        r"Neighbor Down:\s+(.+)",
        message,
        re.IGNORECASE,
    )

    if match:
        result["ospf_neighbor"] = match.group(1)
        result["ospf_interface"] = match.group(2)
        result["ospf_old_state"] = match.group(3)
        result["ospf_new_state"] = match.group(4)
        result["ospf_reason"] = match.group(5)

    return result


def parse_log_file(file_path):
    events = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            event = parse_log_line(line)

            if event:
                events.append(event)

    return events


def parse_all_logs(raw_directory):
    raw_directory = Path(raw_directory)

    all_events = []

    for file_path in sorted(raw_directory.glob("*.log")):
        print(f"Parsing {file_path.name}")

        events = parse_log_file(file_path)
        all_events.extend(events)

    return pd.DataFrame(all_events)   


#test = parse_all_logs("project-2-syslog-analysis/data/raw/") 
#print(test)