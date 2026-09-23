import re

import yaml


def check_ntp(config, baseline):
    server = baseline["ntp"]["server"]

    compliant = bool(
        re.search(
            rf"(?m)^ntp server {re.escape(server)}\s*$",
            config,
        )
    )

    return compliant


def check_tacacs(config, baseline):
    server = baseline["tacacs"]["server"]

    address_present = bool(
        re.search(
            rf"(?m)^\s*address ipv4 {re.escape(server)}\s*$",
            config,
        )
    )

    aaa_present = bool(
        re.search(
            r"(?m)^aaa authentication login default group tacacs\+ local",
            config,
        )
    )

    return address_present and aaa_present


def check_ssh(config, baseline):
    version = baseline["ssh"]["version"]
    return bool(
        re.search(
            rf"(?m)^ip ssh version {version}\s*$",
            config,
        )
    )


def check_syslog(config, baseline):
    server = baseline["syslog"]["server"]

    return bool(
        re.search(
            rf"(?m)^logging host {re.escape(server)}\s*$",
            config,
        )
    )


def check_management_acl(config, baseline):
    acl_name = baseline["management_acl"]["name"]

    if acl_name == "management":
        
        return bool(
            re.search(
                rf"(?m)^\s*access-class {re.escape(acl_name)} in",
                config,
                )
            )


def check_device(device_name, config, baseline):
    checks = {
        "NTP": check_ntp(config, baseline),
        "AAA_TACACS": check_tacacs(config, baseline),
        "SSH_v2": check_ssh(config, baseline),
        "Syslog": check_syslog(config, baseline),
        "Management_ACL": check_management_acl(
            config,
            baseline,
        ),
    }

    rows = []

    for control, result in checks.items():

        if result is None:
            status = "NOT_CONFIGURED"
        elif result:
            status = "COMPLIANT"
        else:
            status = "NON_COMPLIANT"

        rows.append({
            "device": device_name,
            "control": control,
            "status": status,
        })

    return rows



 
#  ----------  TEST  ------------------------

#with open("project-1-inventory-compliance/data/raw/hq-dsw1/running_config.txt", "r", encoding="utf-8") as file:
#    config_t = file.read()

#with open("project-1-inventory-compliance/baseline.yaml", "r", encoding="utf-8") as file:
#    base = yaml.safe_load(file)


#temp = check_ssh(config_t,base)
#print(temp)