#!/usr/bin/env python
"""
NETCONF Get Configuration Example

This script retrieves configuration data from a NETCONF device.
It demonstrates the <get-config> RPC operation.
"""

import sys
import argparse
from ncclient import manager
from lxml import etree

sys.path.append('..')
from utils.defaults import HOST, PORT, USER, PASSWORD
from utils.helpers import write_file


def get_config(host, port, user, password, source='running', filter_xpath=None):
    """
    Retrieve configuration from device.
    
    Args:
        host: Device IP address or hostname
        port: NETCONF port
        user: Username
        password: Password
        source: Configuration datastore ('running', 'candidate', 'startup')
        filter_xpath: Optional XPath filter
    
    Returns:
        XML string of configuration data
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
            config = m.get_config(source=source, filter=('xpath', filter_xpath))
        else:
            config = m.get_config(source=source)
    
    return config.data_xml


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
        description='Retrieve configuration from a NETCONF device'
    )
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=PORT,
                        help=f'NETCONF port (default: {PORT})')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--source', '-s', default='running',
                        choices=['running', 'candidate', 'startup'],
                        help='Configuration datastore (default: running)')
    parser.add_argument('--filter', '-f', default=None,
                        help='XPath filter for configuration')
    parser.add_argument('--output', '-o', default=None,
                        help='Output file (default: print to stdout)')
    
    args = parser.parse_args()
    
    try:
        print(f"Connecting to {args.host}:{args.port}...")
        print(f"Retrieving {args.source} configuration...")
        
        config_xml = get_config(
            args.host, args.port, args.user, args.password,
            args.source, args.filter
        )
        
        formatted_xml = pretty_print_xml(config_xml)
        
        if args.output:
            write_file(args.output, formatted_xml)
        else:
            print("\nConfiguration:\n")
            print(formatted_xml)
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
