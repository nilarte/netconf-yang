#!/usr/bin/env python
"""
NETCONF Edit Configuration Example

This script sends configuration changes to a NETCONF device.
It demonstrates the <edit-config> RPC operation.
"""

import sys
import argparse
from ncclient import manager

sys.path.append('..')
from utils.defaults import HOST, PORT, USER, PASSWORD
from utils.helpers import read_file


def edit_config(host, port, user, password, config_xml, target='running'):
    """
    Send configuration to device.
    
    Args:
        host: Device IP address or hostname
        port: NETCONF port
        user: Username
        password: Password
        config_xml: XML configuration string
        target: Target datastore ('running', 'candidate', 'startup')
    
    Returns:
        RPC reply object
    """
    with manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={'name': 'default'}
    ) as m:
        reply = m.edit_config(target=target, config=config_xml)
    
    return reply


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Send configuration to a NETCONF device'
    )
    parser.add_argument('config_file',
                        help='XML configuration file to send')
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=PORT,
                        help=f'NETCONF port (default: {PORT})')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--target', '-t', default='running',
                        choices=['running', 'candidate', 'startup'],
                        help='Target datastore (default: running)')
    
    args = parser.parse_args()
    
    try:
        print(f"Reading configuration from {args.config_file}...")
        config_xml = read_file(args.config_file)
        
        print(f"Connecting to {args.host}:{args.port}...")
        print(f"Sending configuration to {args.target} datastore...")
        
        reply = edit_config(
            args.host, args.port, args.user, args.password,
            config_xml, args.target
        )
        
        if reply.ok:
            print("\n✓ Configuration successfully applied!")
        else:
            print(f"\n✗ Configuration failed: {reply}")
            return 1
        
        return 0
    except FileNotFoundError:
        print(f"Error: File '{args.config_file}' not found", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
