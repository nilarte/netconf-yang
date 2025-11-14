# YANG Model Examples

This directory contains sample XML configuration files based on standard YANG models.

## Files

### interface_config.xml
Sample configuration for a network interface using the IETF interfaces YANG model.

**Features:**
- Interface description
- IPv4 address configuration
- Enable/disable interface

**Usage:**
```bash
cd ../netconf-basic
python edit_config.py ../yang-models/interface_config.xml
```

### loopback_config.xml
Sample configuration for creating a loopback interface (Cisco IOS-XE specific).

**Features:**
- Loopback interface creation
- IP address assignment
- Description

**Usage:**
```bash
cd ../netconf-basic
python edit_config.py ../yang-models/loopback_config.xml
```

### interface_config.json
Sample JSON configuration for RESTCONF operations. Demonstrates interface configuration in JSON format.

**Usage:**
```bash
cd ../restconf
python restconf_post.py /data/ietf-interfaces:interfaces ../yang-models/interface_config.json
```

## Customization

Modify these XML files to match your device and requirements:
1. Update interface names (e.g., GigabitEthernet1, eth0)
2. Change IP addresses and subnet masks
3. Adjust descriptions and other parameters
4. Ensure XML namespaces match your device's YANG models

## Validation

Before sending to a device:
1. Validate XML syntax
2. Check YANG model compatibility with device
3. Test on a lab device first

## YANG Models Reference

These examples use standard YANG models:
- `ietf-interfaces`: Interface configuration
- `ietf-ip`: IP configuration
- Cisco IOS-XE native models (for Cisco devices)
