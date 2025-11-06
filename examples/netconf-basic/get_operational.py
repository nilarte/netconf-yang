#!/usr/bin/env python
"""
NETCONF Get Operational Data Example

This script retrieves operational (state) data from a NETCONF device.
It demonstrates the <get> RPC operation which retrieves both config and state data.
"""

import sys
import argparse
from ncclient import manager
from lxml import etree

sys.path.append('..')
from utils.defaults import HOST, PORT, USER, PASSWORD
from utils.helpers import write_file


def get_operational_data(host, port, user, password, filter_xpath=None):
    """
    Retrieve operational data from device.
    
    Args:
        host: Device IP address or hostname
        port: NETCONF port
        user: Username
        password: Password
        filter_xpath: Optional XPath filter
    
    Returns:
        XML string of operational data
    """
    with manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={'name': 'default'}
    ) as m:
        if filter_xpath:
            data = m.get(filter=('xpath', filter_xpath))
        else:
            data = m.get()
    
    return data.data_xml


def pretty_print_xml(xml_string):
    """Pretty print XML string."""
    try:
        root = etree.fromstring(xml_string.encode('utf-8'))
        return etree.tostring(root, pretty_print=True, encoding='unicode')
    except Exception as e:
        print(f"Warning: Could not pretty print XML: {e}")
        return xml_string


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Retrieve operational data from a NETCONF device'
    )
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=PORT,
                        help=f'NETCONF port (default: {PORT})')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--filter', '-f', default=None,
                        help='XPath filter for data')
    parser.add_argument('--output', '-o', default=None,
                        help='Output file (default: print to stdout)')
    
    args = parser.parse_args()
    
    try:
        print(f"Connecting to {args.host}:{args.port}...")
        print("Retrieving operational data...")
        
        data_xml = get_operational_data(
            args.host, args.port, args.user, args.password,
            args.filter
        )
        
        formatted_xml = pretty_print_xml(data_xml)
        
        if args.output:
            write_file(args.output, formatted_xml)
        else:
            print("\nOperational Data:\n")
            print(formatted_xml)
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
