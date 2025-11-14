#!/usr/bin/env python
"""
RESTCONF GET Example

This script retrieves configuration or operational data using RESTCONF.
RESTCONF is an HTTP-based protocol that uses YANG models.
"""

import sys
import argparse
import requests
import json
from requests.auth import HTTPBasicAuth

sys.path.append('..')
from utils.defaults import HOST, USER, PASSWORD
from utils.helpers import write_file

# Disable SSL warnings for demo purposes
requests.packages.urllib3.disable_warnings()


def get_restconf_data(host, user, password, path, port=443):
    """
    Retrieve data via RESTCONF.
    
    Args:
        host: Device IP address or hostname
        user: Username
        password: Password
        path: RESTCONF resource path (e.g., '/data/ietf-interfaces:interfaces')
        port: RESTCONF port (default 443)
    
    Returns:
        JSON response data
    """
    url = f"https://{host}:{port}/restconf{path}"
    
    headers = {
        'Accept': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json'
    }
    
    response = requests.get(
        url,
        auth=HTTPBasicAuth(user, password),
        headers=headers,
        verify=False
    )
    
    response.raise_for_status()
    return response.json()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Retrieve data from a RESTCONF device'
    )
    parser.add_argument('path',
                        help='RESTCONF path (e.g., /data/ietf-interfaces:interfaces)')
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=443,
                        help='RESTCONF port (default: 443)')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--output', '-o', default=None,
                        help='Output file (default: print to stdout)')
    
    args = parser.parse_args()
    
    try:
        print(f"Connecting to https://{args.host}:{args.port}...")
        print(f"Retrieving data from {args.path}...")
        
        data = get_restconf_data(
            args.host, args.user, args.password, args.path, args.port
        )
        
        formatted_json = json.dumps(data, indent=2)
        
        if args.output:
            write_file(args.output, formatted_json)
        else:
            print("\nRESTCONF Data:\n")
            print(formatted_json)
        
        return 0
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
