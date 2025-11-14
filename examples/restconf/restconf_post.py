#!/usr/bin/env python
"""
RESTCONF POST/PUT Example

This script demonstrates sending configuration data to a device using RESTCONF:
- POST: Create new resources
- PUT: Replace existing resources
"""

import sys
import argparse
import requests
import json
from requests.auth import HTTPBasicAuth

sys.path.append('..')
from utils.defaults import HOST, USER, PASSWORD
from utils.helpers import read_file

# Disable SSL warnings for demo purposes
requests.packages.urllib3.disable_warnings()


def send_restconf_config(host, user, password, path, data, method='POST', port=443):
    """
    Send configuration via RESTCONF.
    
    Args:
        host: Device IP address or hostname
        user: Username
        password: Password
        path: RESTCONF resource path
        data: JSON or dict data to send
        method: HTTP method ('POST' or 'PUT')
        port: RESTCONF port (default 443)
    
    Returns:
        Response object
    """
    url = f"https://{host}:{port}/restconf{path}"
    
    headers = {
        'Accept': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json'
    }
    
    # Convert string to dict if needed
    if isinstance(data, str):
        data = json.loads(data)
    
    if method.upper() == 'POST':
        response = requests.post(
            url,
            auth=HTTPBasicAuth(user, password),
            headers=headers,
            json=data,
            verify=False
        )
    elif method.upper() == 'PUT':
        response = requests.put(
            url,
            auth=HTTPBasicAuth(user, password),
            headers=headers,
            json=data,
            verify=False
        )
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return response


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Send configuration to a RESTCONF device',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new interface configuration (POST)
  python restconf_post.py /data/ietf-interfaces:interfaces interface.json
  
  # Replace interface configuration (PUT)
  python restconf_post.py /data/ietf-interfaces:interfaces/interface=eth0 \
      interface.json --method PUT
        """
    )
    parser.add_argument('path',
                        help='RESTCONF path (e.g., /data/ietf-interfaces:interfaces)')
    parser.add_argument('data_file',
                        help='JSON file with configuration data')
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=443,
                        help='RESTCONF port (default: 443)')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--method', '-m', default='POST',
                        choices=['POST', 'PUT'],
                        help='HTTP method (default: POST)')
    
    args = parser.parse_args()
    
    try:
        print(f"Reading data from {args.data_file}...")
        data = read_file(args.data_file)
        
        print(f"Connecting to https://{args.host}:{args.port}...")
        print(f"Sending {args.method} request to {args.path}...")
        
        response = send_restconf_config(
            args.host, args.user, args.password, args.path, data,
            args.method, args.port
        )
        
        # Check response
        if response.status_code in [200, 201, 204]:
            print(f"\n✓ Configuration successfully applied!")
            print(f"  Status: {response.status_code}")
            if response.text:
                print(f"  Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"\n✗ Configuration failed!")
            print(f"  Status: {response.status_code}")
            print(f"  Error: {response.text}")
            return 1
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{args.data_file}' not found", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
