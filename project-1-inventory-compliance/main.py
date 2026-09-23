from pathlib import Path

import yaml

from src.collector import load_devices, collect_all
from src.parser import build_dataframes
from src.compliance import check_device
from src.report import generate_reports


BASE_DIR = Path(__file__).resolve().parent

INVENTORY_FILE = BASE_DIR / "devices.yaml"
BASELINE_FILE = BASE_DIR / "baseline.yaml"

RAW_DIRECTORY = BASE_DIR / "data" / "raw"
REPORTS_DIRECTORY = BASE_DIR / "reports"


def load_baseline():
    with open(BASELINE_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    print("=" * 60)
    print("Project Atlas Network Inventory & Compliance Reporter")
    print("=" * 60)

    devices = load_devices(INVENTORY_FILE)
    baseline = load_baseline()

    print(f"\nDevices configured: {len(devices)}")

    collected = collect_all(
        devices,
        RAW_DIRECTORY,
    )

    if not collected:
        print("\nNo devices were successfully collected.")
        return

    dataframes = build_dataframes(collected)

    compliance_rows = []

    for device_name, data in collected.items():
        config = data["output"]["running_config"]

        compliance_rows.extend(
            check_device(
                device_name,
                config,
                baseline,
            )
        )

    generate_reports(
        dataframes,
        compliance_rows,
        REPORTS_DIRECTORY,
    )

    print("\n✓ Project 1 completed successfully.")
    #print("\n  --------------LET US CHECK................ \n ")
    #print(collected["hq-dsw1"]["output"])

if __name__ == "__main__":
    main()