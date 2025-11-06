# NETCONF/YANG Scripts

A collection of representative Python scripts demonstrating NETCONF and YANG operations for network automation. These scripts provide practical examples for interacting with network devices using model-driven programmability.

## Overview

This repository contains example scripts for:
- **NETCONF Operations**: Basic operations like get-config, edit-config, and get capabilities
- **YANG Data Models**: Sample XML configurations based on standard YANG models
- **RESTCONF**: HTTP-based network management using YANG models
- **Utilities**: Helper functions for common operations

## Features

- ✅ **NETCONF Client Examples**: Connect to devices and perform CRUD operations
- ✅ **Standard YANG Models**: Examples using IETF and vendor-specific models
- ✅ **RESTCONF Support**: HTTP-based alternative to NETCONF
- ✅ **Well-documented Code**: Clear examples with comprehensive comments
- ✅ **CLI-ready Scripts**: Command-line tools with argument parsing

## Requirements

- Python 3.7 or higher
- Network device with NETCONF/RESTCONF support (e.g., Cisco IOS-XE, Juniper Junos, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nilarte/netconf-yang.git
cd netconf-yang
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure device parameters in `utils/defaults.py`:
```python
HOST = '192.168.1.1'
PORT = 830
USER = 'admin'
PASSWORD = 'admin'
```

## Usage

### NETCONF Examples

#### Get Device Capabilities
Retrieve the list of YANG models and NETCONF features supported by a device:

```bash
cd examples/netconf-basic
python get_capabilities.py --host 192.168.1.1 --user admin --password admin
```

Filter capabilities by pattern:
```bash
python get_capabilities.py --search "ietf-interfaces"
```

#### Get Configuration
Retrieve the running configuration from a device:

```bash
python get_config.py --host 192.168.1.1 --source running
```

Save configuration to file:
```bash
python get_config.py --source running --output config_backup.xml
```

#### Edit Configuration
Apply configuration changes from an XML file:

```bash
python edit_config.py ../yang-models/interface_config.xml --host 192.168.1.1
```

#### Get Operational Data
Retrieve operational (state) data from the device:

```bash
python get_operational.py --host 192.168.1.1
```

Filter operational data:
```bash
python get_operational.py --filter "/interfaces/interface[name='GigabitEthernet1']"
```

### RESTCONF Examples

#### Get Data via RESTCONF
Retrieve data using RESTCONF (HTTP-based):

```bash
cd examples/restconf
python restconf_get.py /data/ietf-interfaces:interfaces --host 192.168.1.1
```

Save output to file:
```bash
python restconf_get.py /data/ietf-interfaces:interfaces --output interfaces.json
```

## Project Structure

```
netconf-yang/
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore patterns
├── utils/                        # Utility modules
│   ├── __init__.py
│   ├── defaults.py              # Default connection parameters
│   └── helpers.py               # Helper functions
├── examples/
│   ├── netconf-basic/           # Basic NETCONF operations
│   │   ├── get_capabilities.py # Get device capabilities
│   │   ├── get_config.py       # Retrieve configuration
│   │   ├── edit_config.py      # Modify configuration
│   │   └── get_operational.py  # Get operational data
│   ├── restconf/                # RESTCONF examples
│   │   └── restconf_get.py     # GET data via RESTCONF
│   └── yang-models/             # Sample YANG-based configs
│       ├── interface_config.xml # Interface configuration
│       └── loopback_config.xml  # Loopback configuration
```

## Sample XML Configurations

The `examples/yang-models/` directory contains sample XML configurations:

### Interface Configuration
Configure an interface with IP address:
```bash
cd examples/netconf-basic
python edit_config.py ../yang-models/interface_config.xml
```

### Loopback Configuration
Create a loopback interface:
```bash
python edit_config.py ../yang-models/loopback_config.xml
```

## Common NETCONF Operations

| Operation | RPC | Purpose |
|-----------|-----|---------|
| Get Config | `<get-config>` | Retrieve configuration from datastore |
| Edit Config | `<edit-config>` | Modify configuration |
| Get | `<get>` | Retrieve config and operational data |
| Copy Config | `<copy-config>` | Copy between datastores |
| Delete Config | `<delete-config>` | Delete a configuration datastore |
| Lock/Unlock | `<lock>`, `<unlock>` | Lock datastore for exclusive access |
| Commit | `<commit>` | Commit candidate configuration |

## YANG Models

YANG (Yet Another Next Generation) is a data modeling language used to model configuration and state data. Common YANG models include:

- **ietf-interfaces**: Standard interface configuration
- **ietf-ip**: IP address configuration
- **ietf-routing**: Routing configuration
- **openconfig-***: OpenConfig vendor-neutral models
- Vendor-specific models (Cisco, Juniper, etc.)

## Tips and Best Practices

1. **Always test on lab devices first** before production
2. **Use candidate datastore** when available for safe configuration changes
3. **Implement proper error handling** in production scripts
4. **Lock datastores** when making critical configuration changes
5. **Validate configurations** before committing changes
6. **Use filters** to retrieve only necessary data
7. **Keep credentials secure** - don't hardcode passwords in scripts

## Troubleshooting

### Connection Issues
- Verify NETCONF is enabled on the device
- Check firewall rules allow port 830 (NETCONF) or 443 (RESTCONF)
- Confirm SSH/HTTPS access is working
- Verify credentials are correct

### YANG Model Issues
- Check device capabilities to see supported models
- Verify YANG model version compatibility
- Use correct XML namespaces in configurations

### SSL/Certificate Issues (RESTCONF)
- For testing, SSL verification is disabled in examples
- For production, properly configure SSL certificates

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and demonstration purposes.

## Additional Resources

- [RFC 6241 - NETCONF Protocol](https://tools.ietf.org/html/rfc6241)
- [RFC 8040 - RESTCONF Protocol](https://tools.ietf.org/html/rfc8040)
- [RFC 7950 - YANG 1.1](https://tools.ietf.org/html/rfc7950)
- [ncclient Documentation](https://ncclient.readthedocs.io/)
- [YANG Catalog](https://yangcatalog.org/)
- [Cisco DevNet](https://developer.cisco.com/)

## Contact

For questions or issues, please open an issue on GitHub.