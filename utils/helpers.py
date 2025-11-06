"""
Helper functions for file operations and data manipulation.
"""


def write_file(filename, text):
    """Write text content to a file."""
    with open(filename, 'w') as f:
        f.write(text)
    print(f"Written to file: {filename}")


def read_file(filename):
    """Read and return text content from a file."""
    with open(filename, 'r') as f:
        result = f.read()
    return result


def append_to_file(filename, text):
    """Append text content to a file."""
    with open(filename, 'a') as f:
        f.write(text)
