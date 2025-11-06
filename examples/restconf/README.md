# RESTCONF Examples

This directory contains examples for interacting with network devices using RESTCONF, an HTTP-based protocol that provides a programmatic interface for accessing YANG-defined data.

## Scripts

### restconf_get.py
Retrieves configuration or operational data from a device using RESTCONF GET requests.

**Usage:**
```bash
python restconf_get.py /data/ietf-interfaces:interfaces --host 192.168.1.1
python restconf_get.py /data/ietf-interfaces:interfaces --output interfaces.json
```

**Common RESTCONF Paths:**
- `/data/ietf-interfaces:interfaces` - All interfaces
- `/data/ietf-interfaces:interfaces/interface=eth0` - Specific interface
- `/data/ietf-routing:routing` - Routing information
- `/data/ietf-system:system` - System information

## RESTCONF vs NETCONF

| Feature | RESTCONF | NETCONF |
|---------|----------|---------|
| Transport | HTTP/HTTPS | SSH |
| Encoding | JSON/XML | XML |
| Port | 443/80 | 830 |
| Operations | GET, POST, PUT, PATCH, DELETE | RPC-based |

## Prerequisites

Install required packages:
```bash
pip install -r ../../requirements.txt
```

## Notes

- RESTCONF typically uses HTTPS (port 443)
- Authentication uses HTTP Basic Auth
- Responses are in JSON format by default
- SSL certificate verification is disabled in examples for testing
- For production, properly configure SSL certificates

## Example Workflow

1. Discover available resources:
```bash
python restconf_get.py /.well-known/host-meta
```

2. Get all interfaces:
```bash
python restconf_get.py /data/ietf-interfaces:interfaces
```

3. Save output for analysis:
```bash
python restconf_get.py /data/ietf-interfaces:interfaces --output interfaces.json
```
