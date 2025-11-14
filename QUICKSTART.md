# Quick Start Guide

This guide will help you get started with the NETCONF/YANG scripts in under 5 minutes.

## Prerequisites

- Python 3.7 or higher installed
- A NETCONF-enabled network device (or simulator)
- Network connectivity to the device

## Step 1: Install Dependencies

```bash
# Clone the repository
git clone https://github.com/nilarte/netconf-yang.git
cd netconf-yang

# Install required Python packages
pip install -r requirements.txt
```

## Step 2: Configure Device Connection

Edit `utils/defaults.py` with your device information:

```python
HOST = '192.168.1.1'      # Your device IP
PORT = 830                # NETCONF port (usually 830)
USER = 'admin'            # Username
PASSWORD = 'admin'        # Password
```

**Security Note:** For production use, consider using environment variables or secure credential storage instead of hardcoding credentials.

## Step 3: Test Connection

Try getting the device capabilities:

```bash
cd examples/netconf-basic
python get_capabilities.py
```

If successful, you'll see a list of YANG models supported by your device.

## Step 4: Try Basic Operations

### View Current Configuration

```bash
# Get the running configuration
python get_config.py --source running

# Get just interface configuration
python get_filtered.py --preset interfaces
```

### Backup Configuration

```bash
python get_config.py --source running --output backup.xml
```

### Apply Configuration

```bash
# Edit the sample configuration file first to match your device
# examples/yang-models/interface_config.xml

# Then apply it safely
python safe_commit.py ../yang-models/interface_config.xml
```

## Step 5: Explore Advanced Examples

### Complete Workflow with Backup

```bash
python complete_workflow.py ../yang-models/interface_config.xml
```

This will:
1. Connect to the device
2. Check capabilities
3. Backup current configuration
4. Apply your changes
5. Verify the changes

### Using RESTCONF

```bash
cd ../restconf

# Get interfaces via RESTCONF
python restconf_get.py /data/ietf-interfaces:interfaces

# Apply configuration via RESTCONF
python restconf_post.py /data/ietf-interfaces:interfaces ../yang-models/interface_config.json
```

## Common Issues and Solutions

### "ModuleNotFoundError: No module named 'ncclient'"

**Solution:** Install dependencies with `pip install -r requirements.txt`

### "Connection refused" or "Connection timeout"

**Solutions:**
- Verify NETCONF is enabled on the device
- Check firewall rules allow port 830
- Verify the IP address is correct
- Test basic SSH connectivity first

### "Authentication failed"

**Solutions:**
- Verify username and password are correct
- Check if the user has sufficient privileges for NETCONF
- Some devices require special NETCONF user configuration

### "YANG model not found"

**Solutions:**
- Check device capabilities to see supported models: `python get_capabilities.py`
- Use appropriate YANG models for your device
- Update the XML namespace in configuration files

## Next Steps

1. **Read the main README.md** for detailed documentation
2. **Explore example scripts** in `examples/netconf-basic/` and `examples/restconf/`
3. **Customize XML configs** in `examples/yang-models/` for your needs
4. **Check individual README files** in each example directory

## Testing Without a Real Device

If you don't have a NETCONF-enabled device, you can use simulators:

### Option 1: Use Cisco DevNet Sandbox
- Free sandboxes available at https://developer.cisco.com/site/sandbox/
- Always-on IOS XE sandboxes available

### Option 2: Docker-based NETCONF Simulator
```bash
# Example using sysrepo/netopeer2
docker run -d -p 830:830 --name netconf sysrepo/sysrepo-netopeer2:latest
```

### Option 3: Python NETCONF Server
```bash
pip install netconf-console
# Follow netconf-console documentation for setting up a test server
```

## Getting Help

- Check the [main README](README.md) for comprehensive documentation
- Review example scripts - they include detailed comments
- Open an issue on GitHub if you encounter problems

## What to Try Next

Once you're comfortable with the basics:

1. **Modify the example configurations** to match your network topology
2. **Create your own YANG-based configurations**
3. **Build automation scripts** using these examples as building blocks
4. **Integrate with CI/CD pipelines** for automated network configuration
5. **Add error handling and logging** for production use

Happy automating! 🚀
