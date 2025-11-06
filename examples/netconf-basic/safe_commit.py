#!/usr/bin/env python
"""
NETCONF Lock and Commit Example

This script demonstrates how to safely modify configuration using:
1. Lock the candidate datastore
2. Edit the configuration
3. Commit the changes
4. Unlock the datastore

This is the recommended approach for critical configuration changes.
"""

import sys
import argparse
from ncclient import manager

sys.path.append('..')
from utils.defaults import HOST, PORT, USER, PASSWORD
from utils.helpers import read_file


def safe_config_change(host, port, user, password, config_xml):
    """
    Safely modify configuration using lock-edit-commit-unlock pattern.
    
    Args:
        host: Device IP address or hostname
        port: NETCONF port
        user: Username
        password: Password
        config_xml: XML configuration string
    
    Returns:
        Boolean indicating success
    """
    with manager.connect(
        host=host,
        port=port,
        username=user,
        password=password,
        hostkey_verify=False,
        device_params={'name': 'default'}
    ) as m:
        
        # Check if candidate datastore is supported
        if ':candidate' not in m.server_capabilities:
            print("Warning: Candidate datastore not supported by device")
            print("Applying directly to running configuration...")
            reply = m.edit_config(target='running', config=config_xml)
            return reply.ok
        
        try:
            # Step 1: Lock the candidate configuration
            print("1. Locking candidate datastore...")
            m.lock(target='candidate')
            
            # Step 2: Edit the candidate configuration
            print("2. Editing candidate configuration...")
            m.edit_config(target='candidate', config=config_xml)
            
            # Step 3: Commit the candidate to running
            print("3. Committing changes to running configuration...")
            m.commit()
            
            print("✓ Configuration successfully applied!")
            return True
            
        except Exception as e:
            print(f"✗ Error during configuration: {e}")
            # Attempt to discard changes
            try:
                print("Discarding candidate changes...")
                m.discard_changes()
            except:
                pass
            return False
            
        finally:
            # Step 4: Always unlock, even if there was an error
            try:
                print("4. Unlocking candidate datastore...")
                m.unlock(target='candidate')
            except Exception as e:
                print(f"Warning: Could not unlock datastore: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Safely apply configuration using lock-commit pattern'
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
    
    args = parser.parse_args()
    
    try:
        print(f"Reading configuration from {args.config_file}...")
        config_xml = read_file(args.config_file)
        
        print(f"\nConnecting to {args.host}:{args.port}...")
        success = safe_config_change(
            args.host, args.port, args.user, args.password,
            config_xml
        )
        
        return 0 if success else 1
        
    except FileNotFoundError:
        print(f"Error: File '{args.config_file}' not found", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
