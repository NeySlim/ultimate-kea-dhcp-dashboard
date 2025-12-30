# Contributing to Ultimate Kea Dashboard

Thank you for considering contributing to Ultimate Kea Dashboard! 

## How to Contribute

### Reporting Bugs
- Use GitHub Issues
- Include system information (OS, Python version, Kea version)
- Provide clear steps to reproduce
- Include relevant logs

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Explain why it would be valuable

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add AmazingFeature'`)
6. Push to your fork (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Comment complex logic
- Keep functions focused and small

### Testing
- Test on a clean Debian/Ubuntu system
- Verify all themes work correctly
- Check both DHCP tables function properly
- Ensure scanning works as expected

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ultimate-kea-dashboard.git

# Install in development mode
cd ultimate-kea-dashboard
sudo ./installer/install.sh

# Make changes
# Test changes
sudo systemctl restart ultimate-dashboard

# View logs
sudo journalctl -u ultimate-dashboard -f
```

## Questions?

Feel free to open a GitHub Discussion for questions!
