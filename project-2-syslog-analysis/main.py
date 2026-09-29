from pathlib import Path

from src.parser import parse_all_logs
from src.analyzer import create_reports


BASE_DIR = Path(__file__).resolve().parent

RAW_DIRECTORY = BASE_DIR / "data" / "raw"
REPORTS_DIRECTORY = BASE_DIR / "reports"


def main():
    print("=" * 60)
    print("Project Atlas Syslog Analysis")
    print("=" * 60)

    print("\nReading Atlas syslog data...")

    events = parse_all_logs(RAW_DIRECTORY)

    if events.empty:
        print("\nNo valid syslog events were found.")
        return

    print(f"\nEvents parsed: {len(events)}")

    reports = create_reports(
        events,
        REPORTS_DIRECTORY,
    )


    print(f"Reports saved to: {REPORTS_DIRECTORY}")


if __name__ == "__main__":
    main()