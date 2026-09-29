


def create_reports(events, reports_directory):
    reports_directory.mkdir(parents=True, exist_ok=True)

    # Complete parsed dataset
    events.to_csv(
        reports_directory / "syslog_events.csv",
        index=False,
    )

   
    return {
        "events": events,
 
    }