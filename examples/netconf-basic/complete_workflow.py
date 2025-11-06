#!/usr/bin/env python
"""
NETCONF Complete Workflow Example

This script demonstrates a complete NETCONF workflow:
1. Connect and get capabilities
2. Backup current configuration
3. Make configuration changes safely
4. Verify the changes

This is an example of a real-world automation script.
"""

import sys
import argparse
from ncclient import manager
from datetime import datetime
from lxml import etree

sys.path.append('..')
from utils.defaults import HOST, PORT, USER, PASSWORD
from utils.helpers import write_file, read_file


class NetconfWorkflow:
    """Encapsulates a NETCONF workflow."""
    
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self):
        """Establish NETCONF connection."""
        print(f"Connecting to {self.host}:{self.port}...")
        self.connection = manager.connect(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            hostkey_verify=False,
            device_params={'name': 'default'}
        )
        print("✓ Connected successfully")
        return True
    
    def get_capabilities(self):
        """Get and display device capabilities."""
        print("\n--- Device Capabilities ---")
        capabilities = self.connection.server_capabilities
        
        # Filter for YANG models
        yang_models = [c for c in capabilities if '?module=' in c or '?revision=' in c]
        print(f"Device supports {len(yang_models)} YANG models")
        
        # Check for important capabilities
        important = ['candidate', 'validate', 'rollback-on-error', 'confirmed-commit']
        print("\nImportant capabilities:")
        for cap in important:
            status = "✓" if f":{cap}" in str(capabilities) else "✗"
            print(f"  {status} {cap}")
        
        return capabilities
    
    def backup_config(self, filename=None):
        """Backup current running configuration."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backup_{self.host}_{timestamp}.xml"
        
        print(f"\n--- Backing up configuration to {filename} ---")
        config = self.connection.get_config(source='running')
        
        # Pretty print the XML
        root = etree.fromstring(config.data_xml.encode('utf-8'))
        formatted = etree.tostring(root, pretty_print=True, encoding='unicode')
        
        write_file(filename, formatted)
        print(f"✓ Configuration backed up")
        return filename
    
    def apply_config(self, config_xml, use_candidate=True):
        """Apply configuration changes."""
        print("\n--- Applying Configuration ---")
        
        if use_candidate and ':candidate' in self.connection.server_capabilities:
            print("Using candidate datastore...")
            try:
                # Lock candidate
                self.connection.lock(target='candidate')
                
                # Edit config
                self.connection.edit_config(target='candidate', config=config_xml)
                
                # Validate if supported
                if ':validate' in self.connection.server_capabilities:
                    print("Validating configuration...")
                    self.connection.validate(source='candidate')
                
                # Commit
                print("Committing changes...")
                self.connection.commit()
                
                print("✓ Configuration applied successfully")
                return True
                
            except Exception as e:
                print(f"✗ Error: {e}")
                try:
                    print("Discarding changes...")
                    self.connection.discard_changes()
                except:
                    pass
                return False
                
            finally:
                try:
                    self.connection.unlock(target='candidate')
                except:
                    pass
        else:
            print("Applying directly to running configuration...")
            try:
                reply = self.connection.edit_config(target='running', config=config_xml)
                if reply.ok:
                    print("✓ Configuration applied successfully")
                    return True
                else:
                    print(f"✗ Configuration failed: {reply}")
                    return False
            except Exception as e:
                print(f"✗ Error: {e}")
                return False
    
    def verify_config(self, filter_xpath=None):
        """Verify configuration was applied."""
        print("\n--- Verifying Configuration ---")
        if filter_xpath:
            config = self.connection.get_config(
                source='running',
                filter=('xpath', filter_xpath)
            )
        else:
            config = self.connection.get_config(source='running')
        
        print("Current configuration retrieved")
        return config.data_xml
    
    def disconnect(self):
        """Close NETCONF connection."""
        if self.connection:
            self.connection.close_session()
            print("\n✓ Disconnected")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Complete NETCONF workflow demonstration'
    )
    parser.add_argument('config_file',
                        help='XML configuration file to apply')
    parser.add_argument('--host', '-H', default=HOST,
                        help=f'Device hostname or IP (default: {HOST})')
    parser.add_argument('--port', '-p', type=int, default=PORT,
                        help=f'NETCONF port (default: {PORT})')
    parser.add_argument('--user', '-u', default=USER,
                        help=f'Username (default: {USER})')
    parser.add_argument('--password', '-P', default=PASSWORD,
                        help='Password for authentication')
    parser.add_argument('--no-backup', action='store_true',
                        help='Skip configuration backup')
    parser.add_argument('--verify-filter', help='XPath filter for verification')
    
    args = parser.parse_args()
    
    try:
        # Read configuration
        print(f"Reading configuration from {args.config_file}...")
        config_xml = read_file(args.config_file)
        
        # Create workflow
        workflow = NetconfWorkflow(args.host, args.port, args.user, args.password)
        
        # Execute workflow
        workflow.connect()
        workflow.get_capabilities()
        
        if not args.no_backup:
            workflow.backup_config()
        
        success = workflow.apply_config(config_xml)
        
        if success:
            workflow.verify_config(args.verify_filter)
        
        workflow.disconnect()
        
        return 0 if success else 1
        
    except FileNotFoundError:
        print(f"Error: File '{args.config_file}' not found", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
