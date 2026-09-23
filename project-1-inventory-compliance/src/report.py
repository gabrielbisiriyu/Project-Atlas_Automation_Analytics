from pathlib import Path

import pandas as pd


def generate_reports(dataframes, compliance_rows, reports_directory):
    reports_directory = Path(reports_directory)
    reports_directory.mkdir(parents=True, exist_ok=True)

    compliance_df = pd.DataFrame(compliance_rows)

    inventory_df = dataframes["inventory"]
    interfaces_df = dataframes["interfaces"]
    routes_df = dataframes["routes"]
    ospf_df = dataframes["ospf_neighbors"]

    inventory_df.to_csv(
        reports_directory / "inventory.csv",
        index=False,
    )

    interfaces_df.to_csv(
        reports_directory / "interfaces.csv",
        index=False,
    )

    routes_df.to_csv(
        reports_directory / "routes.csv",
        index=False,
    )

    ospf_df.to_csv(
        reports_directory / "ospf_neighbors.csv",
        index=False,
    )

    compliance_df.to_csv(
        reports_directory / "compliance.csv",
        index=False,
    )

   

    print(f"\nReports written to: {reports_directory}")