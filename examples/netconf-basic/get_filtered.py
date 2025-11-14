#!/usr/bin/env python
"""
NETCONF Get with Filter Example

This script demonstrates various filtering techniques to retrieve specific
portions of configuration or operational data:
- Subtree filtering (XML-based)
- XPath filtering
"""

import sys
import argparse
from ncclient import manager
from lxml import etree

sys.path.append('..')
from utils.defaults import HOST, PORT, USER, PASSWORD
from utils.helpers import write_file


# Example subtree filters
FILTER_INTERFACES = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces>
</filter>
"""

FILTER_SYSTEM = """
<filter>
  <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
    <hostname/>
    <clock/>
  </system>
</filter>
"""


def get_filtered_data(host, port, user, password, filter_type='subtree', 
                      filter_content=None, operation='get-config', source='running'):
    """
    Get data with filtering.
    
    Args:
        host: Device IP address or hostname
        port: NETCONF port
        user: Username
        password: Password
        filter_type: 'subtree' or 'xpath'
        filter_content: Filter content (XML string or XPath expression)
        operation: 'get' or 'get-config'
        source: Datastore source (for get-config)
    
    Returns:
        XML string of filtered data
    """
    with manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={'name': 'default'}
    ) as m:
        
        if filter_content:
            if filter_type == 'xpath':
                filter_spec = ('xpath', filter_content)
            else:  # subtree
                filter_spec = ('subtree', filter_content)
        else:
            filter_spec = None
        
        if operation == 'get-config':
            result = m.get_config(source=source, filter=filter_spec)
        else:  # get
            result = m.get(filter=filter_spec)
    
    return result.data_xml


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
        description='Retrieve filtered data from a NETCONF device',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get all interfaces using subtree filter
  python get_filtered.py --preset interfaces
  
  # Get system information
  python get_filtered.py --preset system
  
  # Use XPath filter
  python get_filtered.py --xpath "/interfaces/interface[name='eth0']"
  
  # Get operational data instead of config
  python get_filtered.py --operation get --preset interfaces
        """
    )
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=PORT,
                        help=f'NETCONF port (default: {PORT})')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--preset', choices=['interfaces', 'system'],
                        help='Use a preset filter')
    parser.add_argument('--xpath', help='XPath filter expression')
    parser.add_argument('--subtree', help='Subtree filter (XML string)')
    parser.add_argument('--operation', default='get-config',
                        choices=['get', 'get-config'],
                        help='NETCONF operation (default: get-config)')
    parser.add_argument('--source', default='running',
                        choices=['running', 'candidate', 'startup'],
                        help='Datastore source (default: running)')
    parser.add_argument('--output', '-o', help='Output file')
    
    args = parser.parse_args()
    
    # Determine filter type and content
    if args.preset == 'interfaces':
        filter_type = 'subtree'
        filter_content = FILTER_INTERFACES
    elif args.preset == 'system':
        filter_type = 'subtree'
        filter_content = FILTER_SYSTEM
    elif args.xpath:
        filter_type = 'xpath'
        filter_content = args.xpath
    elif args.subtree:
        filter_type = 'subtree'
        filter_content = args.subtree
    else:
        print("Error: Must specify --preset, --xpath, or --subtree", file=sys.stderr)
        return 1
    
    try:
        print(f"Connecting to {args.host}:{args.port}...")
        print(f"Using {filter_type} filter...")
        
        data_xml = get_filtered_data(
            args.host, args.port, args.user, args.password,
            filter_type, filter_content, args.operation, args.source
        )
        
        formatted_xml = pretty_print_xml(data_xml)
        
        if args.output:
            write_file(args.output, formatted_xml)
        else:
            print("\nFiltered Data:\n")
            print(formatted_xml)
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
