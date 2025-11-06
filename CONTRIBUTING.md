# Contributing to NETCONF-YANG Scripts

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the GitHub Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS, device type)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/nilarte/netconf-yang.git
   cd netconf-yang
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments and docstrings
   - Update relevant documentation

4. **Test your changes**
   ```bash
   # Verify Python syntax
   python3 -m py_compile your_script.py
   
   # Test with a device/simulator if possible
   python3 your_script.py --help
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Guidelines

### Python Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Include type hints where appropriate

Example:
```python
def get_config(host: str, port: int, user: str, password: str) -> str:
    """
    Retrieve configuration from device.
    
    Args:
        host: Device IP address or hostname
        port: NETCONF port
        user: Username
        password: Password
    
    Returns:
        XML string of configuration data
    """
    # Implementation
```

### Script Structure

All scripts should follow this structure:

1. Shebang and module docstring
2. Imports (stdlib, third-party, local)
3. Constants/configuration
4. Helper functions
5. Main function
6. `if __name__ == '__main__'` block

### Documentation

- Update README.md if adding new features
- Add comments for complex logic
- Include usage examples in docstrings
- Update QUICKSTART.md if it affects quick start workflow

## What to Contribute

We welcome contributions in these areas:

### New Examples

- Additional NETCONF operations (validate, copy-config, etc.)
- More YANG model examples
- Device-specific examples (Cisco, Juniper, etc.)
- Error handling patterns
- Logging examples

### Improvements

- Better error messages
- Code optimization
- Additional command-line options
- More comprehensive filtering examples

### Documentation

- Tutorial articles
- Video walkthrough scripts
- Troubleshooting guides
- Device-specific setup guides

### Testing

- Unit tests
- Integration tests
- CI/CD pipeline setup

## Code Review Process

1. All changes require review before merging
2. Reviewers will check:
   - Code quality and style
   - Documentation completeness
   - Backwards compatibility
   - Security implications

## Security

- Never commit credentials or sensitive data
- Use environment variables for secrets in examples
- Report security issues privately to maintainers

## Questions?

Feel free to open an issue for questions or clarifications.

## Thank You!

Your contributions help make network automation more accessible to everyone.
