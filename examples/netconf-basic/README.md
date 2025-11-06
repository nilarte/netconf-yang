# NETCONF Basic Operations

This directory contains fundamental NETCONF client examples demonstrating core operations.

## Scripts

### get_capabilities.py
Connects to a NETCONF device and retrieves its capabilities (supported YANG models and features).

**Usage:**
```bash
python get_capabilities.py --host 192.168.1.1 --user admin --password admin
python get_capabilities.py --search "ietf"  # Filter by pattern
```

### get_config.py
Retrieves configuration data from a specified datastore (running, candidate, or startup).

**Usage:**
```bash
python get_config.py --source running --output backup.xml
python get_config.py --filter "/interfaces"  # XPath filter
```

### edit_config.py
Sends configuration changes to the device from an XML file.

**Usage:**
```bash
python edit_config.py ../yang-models/interface_config.xml
python edit_config.py config.xml --target candidate
```

### get_operational.py
Retrieves both configuration and operational state data from the device.

**Usage:**
```bash
python get_operational.py --output operational.xml
python get_operational.py --filter "/interfaces-state"
```

### get_filtered.py
Demonstrates advanced filtering techniques (subtree and XPath) to retrieve specific data.

**Usage:**
```bash
python get_filtered.py --preset interfaces
python get_filtered.py --xpath "/interfaces/interface[name='eth0']"
python get_filtered.py --operation get --preset system
```

### safe_commit.py
Implements the recommended lock-edit-commit-unlock pattern for safe configuration changes.

**Usage:**
```bash
python safe_commit.py ../yang-models/interface_config.xml
```

### complete_workflow.py
Comprehensive example demonstrating a complete automation workflow including backup, apply, and verify.

**Usage:**
```bash
python complete_workflow.py ../yang-models/interface_config.xml
python complete_workflow.py config.xml --no-backup
```

## Prerequisites

Install required packages:
```bash
pip install -r ../../requirements.txt
```

Configure device parameters in `../../utils/defaults.py` or use command-line arguments.

## Notes

- All scripts support `--help` for detailed usage information
- Default connection parameters can be overridden via command-line arguments
- XML output can be saved to file using `--output` option
