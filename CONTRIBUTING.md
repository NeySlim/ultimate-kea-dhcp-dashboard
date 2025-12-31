# Contributing to Ultimate DHCP Dashboard

## Code Organization

The project follows a modular architecture:

- `bin/ultimate-dashboard` - Main application entry point and HTTP server
- `lib/network_scanner.py` - Network scanning and service discovery
- `lib/device_detection.py` - Device type classification logic
- `lib/mac_vendor.py` - MAC address vendor lookup utilities
- `lib/stats.py` - System statistics collection
- `lib/themes.py` - UI theme definitions
- `static/js/` - Client-side JavaScript components
- `etc/` - Configuration files

## Development Setup

1. Clone the repository
2. Copy `etc/ultimate-dashboard.conf.example` to `etc/ultimate-dashboard.conf`
3. Configure your environment-specific settings
4. Install dependencies: `pip3 install psutil`

## Code Style

- Follow PEP 8 guidelines for Python code
- Use descriptive function and variable names
- Add docstrings to all functions
- Keep functions focused and modular
- Avoid hardcoded credentials or paths

## Security Best Practices

- Never commit sensitive data (passwords, tokens, certificates)
- Use placeholder values in example configurations
- Sanitize user inputs before processing
- Follow principle of least privilege for file permissions

## Testing Changes

Before submitting changes:

1. Test syntax: `python3 -m py_compile bin/ultimate-dashboard`
2. Test all modules: `python3 -m py_compile lib/*.py`
3. Verify configuration loading works correctly
4. Test dashboard accessibility and functionality
5. Check for memory leaks in long-running processes

## Pull Request Guidelines

- Provide clear description of changes
- Reference any related issues
- Ensure code passes syntax checks
- Update documentation if needed
- Test on target environment before submitting

## Reporting Issues

When reporting bugs, include:
- Operating system and Python version
- ISC Kea DHCP version
- Complete error messages and stack traces
- Steps to reproduce the issue
- Configuration details (sanitized)
