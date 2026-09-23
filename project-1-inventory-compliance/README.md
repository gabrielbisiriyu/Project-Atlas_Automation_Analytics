# Network Inventory & Configuration Compliance Reporter

## Overview

A Python-based network inventory and configuration compliance tool built using Project Atlas as a simulated enterprise network.

The project connects to Cisco network devices using Netmiko, collects operational and configuration data, parses the results into Pandas DataFrames, and evaluates devices against a defined configuration baseline.

The tool generates CSV datasets.



## Data Collected

The collector retrieves:

* Running configuration
* IOS version
* Hostname
* Interface status
* Routing table
* OSPF neighbour information

Raw command output is retained for traceability and troubleshooting.

## Compliance Checks

Devices are evaluated against a defined baseline for:

* NTP configuration
* TACACS+ / AAA
* SSH version 2
* Centralized Syslog
* Management ACL

The baseline is stored separately from the application logic so that compliance requirements can be changed without modifying the collection code.

## Technologies

* Python
* Netmiko
* Pandas
* PyYAML
* Cisco IOS
* EVE-NG
* Project Atlas

## Output

The application generates:

* Device inventory CSV
* Interface data CSV
* Routing data CSV
* OSPF neighbour CSV
* Configuration compliance CSV


