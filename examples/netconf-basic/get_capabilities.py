#!/usr/bin/env python
"""
NETCONF Get Capabilities Example

This script connects to a NETCONF-enabled device and retrieves its capabilities.
Capabilities indicate which YANG models and NETCONF features are supported.
"""

import sys
import argparse
import re
from ncclient import manager

# Add parent directory to path for imports
sys.path.append('..')
from utils.defaults import HOST, PORT, USER, PASSWORD


def get_capabilities(host, port, user, password):
    """
    Connect to device and retrieve NETCONF capabilities.
    
    Args:
        host: Device IP address or hostname
        port: NETCONF port (default 830)
        user: Username for authentication
        password: Password for authentication
    
    Returns:
        List of capability strings
    """
    with manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={'name': 'default'}
    ) as m:
        capabilities = m.server_capabilities
    
    return capabilities


def print_capabilities(capabilities, pattern=''):
    """
    Print capabilities, optionally filtered by search pattern.
    
    Args:
        capabilities: List of capability strings
        pattern: Optional regex pattern to filter capabilities
    """
    if pattern:
        print(f"Search pattern: {pattern}")
        filtered = [c for c in capabilities if re.search(pattern, c, re.IGNORECASE)]
    else:
        filtered = capabilities
    
    print(f"\nFound {len(filtered)} capabilities:\n")
    for cap in sorted(filtered):
        print(f"  {cap}")


def main():
    """Main function to parse arguments and get capabilities."""
    parser = argparse.ArgumentParser(
        description='Retrieve NETCONF capabilities from a network device'
    )
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=PORT,
                        help=f'NETCONF port (default: {PORT})')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--search', '-s', default='',
                        help='Filter capabilities by regex pattern')
    
    args = parser.parse_args()
    
    try:
        print(f"Connecting to {args.host}:{args.port}...")
        capabilities = get_capabilities(args.host, args.port, args.user, args.password)
        print_capabilities(capabilities, args.search)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
